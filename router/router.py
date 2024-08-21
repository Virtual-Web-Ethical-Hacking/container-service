import requests
from dotenv import dotenv_values

from fastapi import APIRouter, status, Depends, UploadFile
from fastapi.responses import JSONResponse

from utils.docker.docker import start_container, stop_container, build_images, get_container_info
from utils.utils import change_dockerfile
from utils.authorization.admin_authorization import AdminAuthorization
from utils.authorization.user_authorization import UserAuthorization
from utils.authorization.general_authorization import GeneralAuthorization
from models.models import ContainerInformation

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World from Instance"}


# Hanya bisa admin
@router.get("/info/{container_id}")
async def infoContainer(container_id: str, _: str = Depends(AdminAuthorization())):
    # Stop and delete the container
    try:
        result = get_container_info(container_id)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"data": result}
        )
    
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Error occured"}
        )

# Hanya bisa user
# Belum selsai, tinggal masukin username dan password saja
@router.post("/start")
async def startContainer(creds: ContainerInformation, token: str = Depends(UserAuthorization())):
    # Create container and start (input creds for login (username, and password))
    # Return container id
    try:
        # Getting user info
        config = dotenv_values(".env")
        USER_API = config["USER_API"]

        req = requests.get(
            f"{USER_API}/management/profile",
            headers = {
                "Authorization": f"Bearer {token}"
            }
        )

        container_id = start_container(req.json()["npm"])
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"container_id": container_id}
        )
    
    except:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Error occured"}
        )

# Bisa user dan admin
@router.delete("/stop/{container_id}")
async def stopContainer(container_id: str, data: str = Depends(GeneralAuthorization())):
    # Stop and delete the container
    try:
        # Getting user info
        config = dotenv_values(".env")
        USER_API = config["USER_API"]

        req = requests.post(
            f"{USER_API}/management/profile",
            headers = {
                "Authorization": f"Bearer {data['token']}"
            }
        )

        stop_container(container_id, req.json()["npm"], data["is_admin"])

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
async def updateImages(file: UploadFile, _: str = Depends(AdminAuthorization())):
    # Update image from Dockerfile
    try:
        change_dockerfile(file.file.read().decode())
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
async def read(_: str = Depends(AdminAuthorization())):
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
