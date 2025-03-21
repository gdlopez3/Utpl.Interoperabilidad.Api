from fastapi.security import HTTPBasicCredentials
from fastapi import HTTPException, Depends

def authenticate(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password
   
    if not (username == "admin" and password == "admin"):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return username
