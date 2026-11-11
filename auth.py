from fastapi import Header, HTTPException, status

API_KEY = "0daa79ae6b07cc05a8d4ea08243ea2e2"


def verify_api_key(x_api_key: str = Header()):
    """Verify the API Key from the request header.!"""

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid API Key.!"
        )

    return x_api_key
