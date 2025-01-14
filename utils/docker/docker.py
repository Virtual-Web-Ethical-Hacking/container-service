import docker
from datetime import datetime, timezone, timedelta

from env import IMAGES_NAME, DOCKER_CLIENT

image_name = IMAGES_NAME

CLIENT = docker.APIClient(base_url=DOCKER_CLIENT, use_ssh_client=False)


def get_container_info(container_id: str):
    container = CLIENT.containers(all=True, filters={"id": container_id})[0]

    return [
        { "key": "Container ID", "value": container["Id"] },
        { "key": "Container Name", "value": container["Names"][0] },
        { "key": "Images ID", "value": container["ImageID"] },
        { "key": "Images Name", "value": container["Image"] },
        { "key": "Port", "value": container["Ports"][0]["PublicPort"] },
        { "key": "Created", "value": str(datetime.fromtimestamp(container["Created"], tz=timezone(timedelta(hours=7)))) },
        { "key": "Owner", "value": container["Id"] }
    ]

def start_container(name: str, port: int):
    # Create and start the container
    # Return the container id
    # Nama container menggunakan NPM
    container = CLIENT.create_container(
                    ports=[80],
                    host_config=CLIENT.create_host_config(port_bindings={
                        80: port,
                    }),
                    image=image_name,
                    name=name,
                    detach=True,
                    tty=True,
                )
    
    CLIENT.start(container=container.get('Id'))

    return container.get('Id')


def stop_container(container_id: str, name: str, is_admin: bool):
    # Cek apakah name sama dengan nama container
    # Stop and delete container based on ID

    if not is_admin:
        get_container = CLIENT.containers(filters={'name': name})
        if get_container:
            if str(get_container[0].id) != container_id:
                raise Exception()

    CLIENT.stop(container_id)
    CLIENT.remove_container(container_id)


def build_images():
    # Build images
    [line for line in CLIENT.build(
        path="utils/docker/", rm=True, tag=image_name
    )]