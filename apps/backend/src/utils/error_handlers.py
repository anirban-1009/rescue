from fastapi.responses import JSONResponse


def ErrorResponseModel(error: str, code: int, message: str):
    return JSONResponse(
        status_code=code, content={"error": error, "code": code, "message": message}
    )
