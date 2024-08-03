import docker
from dotenv import dotenv_values

config = dotenv_values(".env")
image_name = config["IMAGES_NAME"]

# CLIENT = docker.APIClient(base_url="tcp://127.0.0.1:2375")
CLIENT = "Fa"

def start_container():
    # Create and start the container
    # Return the container id
    container = CLIENT.create_container(
                    image=image_name,
                    command="/bin/sh",
                    detach=True,
                    tty=True,
                )
    
    CLIENT.start(container=container.get('Id'))

    return container.get('Id')


def stop_container(container_id: str):
    # Stop and delete container based on ID
    CLIENT.stop(container_id)
    CLIENT.remove_container(container_id)


def build_images():
    # Build images
    [line for line in CLIENT.build(
        path="utils/docker/", rm=True, tag=image_name
    )]