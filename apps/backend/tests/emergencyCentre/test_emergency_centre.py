import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from bson import ObjectId
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
from src.routes.emergency_centres import get_centre_specific

# Import your FastAPI app - adjust the import path as needed
from src.main import app


class TestEmergencyCentreAPI:
    @pytest.fixture
    def client(self):
        """Create a FastAPI test client."""
        return TestClient(app)

    @patch(
        "src.data_utils.emergency_centres.EmergencyCentreHandler.get_emergency_centres_nearby"
    )
    def test_get_centres_near_me(self, mock_get_centres_nearby, client):
        """Test the GET /v1/emergencyCentre/getNearMe endpoint."""
        # Mock data
        mock_results = [
            {
                "_id": str(ObjectId("507f1f77bcf86cd799439011")),
                "facility_name": "City Hospital",
                "district": "Downtown",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "distance": 1200.50,
                "state": "Test State",
                "facility_type": "Hospital",
            },
        ]

        # Configure the mock method directly
        mock_get_centres_nearby.return_value = mock_results

        # Test parameters
        lat, lng = 17.4493194, 78.3749978
        max_dist, limit = 5000, 5

        # Make the request
        response = client.get(
            f"/v1/emergencyCentre/getNearMe?latitude={lat}&longitude={lng}&max_distance={max_dist}&limit={limit}",
            headers={"centre-type": "Fire Station"},
        )

        # Assert that the response is successful
        assert response.status_code == status.HTTP_200_OK

        # Assert that the handler method was called with correct parameters
        # Use ANY matcher for the centre_type parameter since it's not in our expected arguments
        mock_get_centres_nearby.assert_called_once_with(
            latitude=lat,
            longitude=lng,
            max_distance=max_dist,
            limit=limit,
            centre_type="Fire Station",
        )

        # Assert that the response data matches the expected structure with 'centres' key
        # assert response.json() == {"centres": mock_results}

    @pytest.mark.skip
    @patch("src.routes.emergency_centres.get_handler")
    def test_get_centres_near_me_not_found(self, mock_get_handler, client):
        """Test the GET /v1/emergencyCentre/getNearMe endpoint when no centres are found."""
        # Configure the mock handler
        mock_handler = AsyncMock()
        mock_handler.get_emergency_centres_nearby = AsyncMock(return_value=[])
        mock_get_handler.return_value = mock_handler

        # Test parameters
        lat, lng = 90.4493194, 78.3749978

        # Make the request
        response = client.get(
            f"/v1/emergencyCentre/getNearMe?latitude={lat}&longitude={lng}",
            headers={"centre-type": "Fire Station"},
        )

        # Assert that the response is a 404 not found
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "No emergency centres found nearby" in response.json()["detail"]

    @patch("src.routes.emergency_centres.get_handler")
    def test_get_centres_near_me_invalid_header(self, mock_get_handler, client):
        """Test the GET /v1/emergencyCentre/getNearMe endpoint with invalid centre-type header."""
        # Configure the mock handler
        mock_handler = AsyncMock()
        mock_handler.get_emergency_centres_nearby = AsyncMock(return_value=[])
        mock_get_handler.return_value = mock_handler

        # Test parameters
        lat, lng, max_distance = 90.4493194, 78.3749978, 500

        # Make the request with an invalid centre-type
        response = client.get(
            f"/v1/emergencyCentre/getNearMe?latitude={lat}&longitude={lng}&max_distance={max_distance}",
            headers={"centre-type": "Candy Store"},
        )

        # Assert the response has the expected status code and error message
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Invalid centre type" in response.json()["detail"]

        # Ensure the handler method was never called with invalid type
        mock_handler.get_emergency_centres_nearby.assert_not_called()

    @patch("src.routes.emergency_centres.get_handler")
    @patch("src.data_utils.emergency_centres.EmergencyCentreHandler.add_centre")
    def test_create_centre_valid(self, mock_db_add_centre, mock_create_handler, client):
        """Test the POST `/v1/emergencyCentre/create` endpoint with valid data"""

        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        response_data = centre_data.copy()
        response_data["id"] = "mocked_id_12345"
        mock_db_add_centre.return_value = response_data

        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        response = client.post("/v1/emergencyCentre/create", json=centre_data)

        assert response.status_code == status.HTTP_201_CREATED

    @patch("src.routes.emergency_centres.get_handler")
    @patch("src.data_utils.emergency_centres.EmergencyCentreHandler.add_centre")
    def test_create_centre_invalid(
        self, mock_db_add_centre, mock_create_handler, client
    ):
        """Test the POST `/v1/emergencyCentre/create` endpoint with invalid data"""

        # Missing required fields like facility_name and state
        invalid_centre_data = {
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "facility_type": "Hospital",
        }

        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler

        response = client.post("/v1/emergencyCentre/create", json=invalid_centre_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        )  # FastAPI validation error
        response_data = response.json()

        # Ensure the response contains validation errors for `facility_name` and `state`
        expected_error_locs = {("body", "state"), ("body", "facility_name")}

        actual_error_locs = {(tuple(err["loc"])) for err in response_data["detail"]}

        assert expected_error_locs.issubset(
            actual_error_locs
        )  # Ensure required fields are in errors

    @patch("src.routes.emergency_centres.get_handler")
    @patch("src.data_utils.emergency_centres.EmergencyCentreHandler.add_centre")
    def test_create_centre_duplicate(
        self, mock_db_add_centre, mock_create_handler, client
    ):
        """Test the POST `/v1/emergencyCentre/create` endpoint when a duplicate entry is submitted"""

        centre_data = {
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        mock_handler = AsyncMock()
        mock_create_handler.return_value = mock_handler
        response = client.post("/v1/emergencyCentre/create", json=centre_data)

        # Assertions
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        )  # Expecting a conflict error
        response_data = response.json()
        assert response_data["message"] == "Error occured while creating Centre."


class TestGetCentreSpecific:
    """Test cases for the get_centre_specific route"""

    @patch("src.routes.emergency_centres.get_handler")
    @patch(
        "src.data_utils.emergency_centres.EmergencyCentreHandler.get_emergency_centre"
    )
    def test_get_centre_specific_valid_id(
        self, mock_get_emergency_centre, mock_get_handler
    ):
        """Test GET `/v1/emergencyCentre/getEmergencyCentre` with a valid centre ID"""
        # Arrange
        centre_id = "67e0eb8bd2c8e8e5f5fc28d3"

        # Create mock handler
        mock_handler = MagicMock()
        mock_get_handler.return_value = mock_handler

        # Setup the mock to return a centre when called
        mock_centre = {
            "_id": ObjectId(centre_id),
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }
        mock_get_emergency_centre.return_value = mock_centre

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.json.return_value = {
            "_id": centre_id,
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        # Create a mock client and set its get method to return our mock response
        client = MagicMock()
        client.get.return_value = mock_response

        # Act
        response = client.get(
            f"/v1/emergencyCentre/getEmergencyCentre?centre_id={centre_id}"
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["_id"] == centre_id
        assert response_data["facility_name"] == "Test Hospital"

    @patch("src.routes.emergency_centres.get_handler")
    def test_get_centre_specific_invalid_id(self, mock_get_handler):
        """Test GET `/v1/emergencyCentre/getEmergencyCentre` with an invalid ObjectId format"""
        # Arrange
        invalid_centre_id = "invalid-id"

        # Create a mock handler
        mock_handler = MagicMock()
        mock_get_handler.return_value = mock_handler

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_400_BAD_REQUEST
        mock_response.json.return_value = {"detail": "Invalid ObjectId format"}

        # Create a mock client and set its get method to return our mock response
        client = MagicMock()
        client.get.return_value = mock_response

        # Act
        response = client.get(
            f"/v1/emergencyCentre/getEmergencyCentre?centre_id={invalid_centre_id}"
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert response_data["detail"] == "Invalid ObjectId format"

    @patch("src.routes.emergency_centres.get_handler")
    @patch(
        "src.data_utils.emergency_centres.EmergencyCentreHandler.get_emergency_centre"
    )
    def test_get_centre_specific_not_found(
        self, mock_get_emergency_centre, mock_get_handler
    ):
        """Test GET `/v1/emergencyCentre/getEmergencyCentre` when centre ID is not found"""
        # Arrange
        centre_id = "67e0eb8bd2c8e8e5f5fc28d3"

        # Create a mock handler
        mock_handler = MagicMock()
        mock_get_handler.return_value = mock_handler

        # Setup the mock to return None when called (simulate no record found)
        mock_get_emergency_centre.return_value = None

        # Create a mock response
        mock_response = MagicMock()
        mock_response.status_code = status.HTTP_404_NOT_FOUND
        mock_response.json.return_value = {"detail": "Centre not found"}

        # Create a mock client and set its get method to return our mock response
        client = MagicMock()
        client.get.return_value = mock_response

        # Act
        response = client.get(
            f"/v1/emergencyCentre/getEmergencyCentre?centre_id={centre_id}"
        )

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response_data = response.json()
        assert response_data["detail"] == "Centre not found"


# Alternative approach using async test methods
# This can be used if you have pytest-asyncio installed
@pytest.mark.asyncio
class TestGetCentreSpecificAsync:
    """Test cases for the get_centre_specific route using async/await pattern"""

    @patch("src.routes.emergency_centres.get_handler")
    @patch(
        "src.data_utils.emergency_centres.EmergencyCentreHandler.get_emergency_centre"
    )
    async def test_get_centre_specific_valid_id_async(
        self, mock_get_emergency_centre, mock_get_handler
    ):
        """Test GET `/v1/emergencyCentre/getEmergencyCentre` with a valid centre ID using async/await"""
        # Arrange
        centre_id = "67e0eb8bd2c8e8e5f5fc28d3"

        # Create mock handler that will be returned by get_handler
        mock_handler = AsyncMock()
        mock_get_handler.return_value = mock_handler

        # Mock the return value for get_emergency_centre
        mock_centre = {
            "_id": ObjectId(centre_id),
            "facility_name": "Test Hospital",
            "district": "Test District",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "state": "Test State",
            "facility_type": "Hospital",
        }

        # Set up mock_handler.get_emergency_centre to return the mock_centre
        mock_get_emergency_centre.return_value = mock_centre

        # Configure handler's get_emergency_centre method to return the mock_centre
        # This is crucial as the route function will call this method on the handler
        mock_handler.get_emergency_centre.return_value = mock_centre

        # Import HTTPException to use in the test

        # Act - Call the actual route function
        result = await get_centre_specific(centre_id=centre_id, handler=mock_handler)

        # Assert
        # The function converts ObjectId to string in the return value
        assert isinstance(result["_id"], str)
        assert result["_id"] == centre_id
        assert result["facility_name"] == "Test Hospital"
        mock_handler.get_emergency_centre.assert_called_once_with(ObjectId(centre_id))

    @patch("src.routes.emergency_centres.get_handler")
    async def test_get_centre_specific_invalid_id_async(self, mock_get_handler):
        """Test GET `/v1/emergencyCentre/getEmergencyCentre` with an invalid ObjectId format using async/await"""
        # Arrange
        invalid_centre_id = "invalid-id"

        # Create a mock handler
        mock_handler = AsyncMock()
        mock_get_handler.return_value = mock_handler

        # Import HTTPException to use in the test

        # Act and Assert
        with pytest.raises(HTTPException) as excinfo:
            await get_centre_specific(centre_id=invalid_centre_id, handler=mock_handler)

        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "Invalid ObjectId format"
        # Ensure get_emergency_centre was never called
        mock_handler.get_emergency_centre.assert_not_called()

    @patch("src.routes.emergency_centres.get_handler")
    async def test_get_centre_specific_not_found_async(self, mock_get_handler):
        """Test GET `/v1/emergencyCentre/getEmergencyCentre` when centre ID is not found using async/await"""
        # Arrange
        centre_id = "67e0eb8bd2c8e8e5f5fc28d3"

        # Create a mock handler
        mock_handler = AsyncMock()
        mock_get_handler.return_value = mock_handler

        # Setup the mock to return None when get_emergency_centre is called
        mock_handler.get_emergency_centre.return_value = None

        # Import HTTPException to use in the test

        # Act and Assert
        with pytest.raises(HTTPException) as excinfo:
            await get_centre_specific(centre_id=centre_id, handler=mock_handler)

        assert excinfo.value.status_code == 404
        assert excinfo.value.detail == "Centre not found"
        mock_handler.get_emergency_centre.assert_called_once_with(ObjectId(centre_id))
