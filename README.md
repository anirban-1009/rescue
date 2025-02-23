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

## References

### Auth0
- [NextJs Auth0 SDK Documentation](https://github.com/auth0/nextjs-auth0/blob/main/EXAMPLES.md)
- [Stych RBAC](https://stytch.com/docs/guides/authorization/rbac)
- [RBAC Auth0 Reference](http://auth0.com/blog/assign-default-role-on-sign-up-with-actions/)
- [RBAC Youtube Video](https://youtu.be/1-kq6llhQDI)
- [Flask Auth0 Reference](https://auth0.com/blog/build-and-secure-fastapi-server-with-auth0/)

### MongoDB

- [Mongo DB Community documentation](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
- [Mongo DB Fast API Tutorial](https://www.mongodb.com/developer/languages/python/python-quickstart-fastapi/)
