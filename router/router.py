from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from utils.docker.docker import start_container, stop_container, build_images
from utils.utils import change_dockerfile
from utils.jwt.user_bearer import UserBearer
from utils.jwt.admin_bearer import AdminBearer
from utils.jwt.auth_bearer import JWTBearer
from models.models import Dockerfile


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World from Instance"}

# Hanya bisa user
@router.get("/start")
async def startContainer(token: str = Depends(UserBearer())):
    # Create container and start
    # Return container id, creds for login (username, and password)
    try:
        container_id = start_container()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Your container id is {container_id}"}
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Error occured"}
        )

# Bisa user dan admin
@router.get("/stop/{container_id}")
async def stopContainer(container_id, token: str = Depends(JWTBearer())):
    # Stop and delete the container
    try:
        stop_container(container_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Container {container_id} is deleted"}
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Error occured"}
        )

# Hanya Admin
@router.post("/update-images")
async def updateImages(data: Dockerfile, token: str = Depends(AdminBearer())):
    # Update image from Dockerfile
    try:
        change_dockerfile(data.text)
        build_images()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Build images success"}
        )
    
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Error occured"}
        )

# Hanya admin
@router.get("/read-dockerfile")
async def read(token: str = Depends(AdminBearer())):
    # Read dockefile
    try:
        f = open("utils/docker/Dockerfile", "r")
        text = f.read()
        f.close()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"dockerfile": text}
        )
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Error occured"}
        )