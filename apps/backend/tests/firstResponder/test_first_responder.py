import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.data_utils.emergency_centres import EmergencyCentreHandler


class TestEmergencyCentreHandler:
    @pytest.fixture
    def mock_emergency_handler(self):
        """Mock the EmergencyCentreHandler with a patched database connection."""
        with patch(
            "src.data_utils.emergency_centres.EmergencyCentreHandler.__init__",
            return_value=None,
        ):
            handler = EmergencyCentreHandler()
            handler.database = MagicMock()

            # Create a properly structured mock for aggregate
            aggregate_mock = MagicMock()
            to_list_mock = AsyncMock()
            aggregate_mock.return_value.to_list = to_list_mock

            handler.collection = MagicMock()
            handler.collection.aggregate = aggregate_mock
            handler.collection.insert_one = AsyncMock()
            handler.collection.find_one = AsyncMock()

            return handler

    # @pytest.mark.asyncio
