from fastapi import status


def success_response(message: str, data=None):
    return {"success": True, "message": message, "data": data}


def error_response(message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    return {"success": False, "message": message}
