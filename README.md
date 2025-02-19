# Rescue

An uniform platform to manage, the resposne of first responders to incidents, and managing the resources.

## Installation

### Python

1. Create Virtual environment

    ``` bash 
    python -m venv .venv
    ```

2. Activate virtual environment

    ```bash
    source .venv/bin/activate
    ```

3. Install pre-requisite libraries
    ```bash
    pip install -r requirements.txt
    ```

### Node

1. Installing monorepo dependencies
    ```bash
    npm install
    ```

2. Installing Frontend dependencies
    * Navigate to the frontend application

        ```bash
        cd frontend/
        ```
    
    * Install the dependencies
        ```bash
        npm install
        ```

## Starting Local Instance

1. Ensure the virtual environment is activated else refer to [Python Section](#python)

2. Initiate Local instance
    ```bash
    npm run dev
    ```

## Running Tests

To run the tests, use the following command:

```bash
pytest
```

