def change_dockerfile(text: str):
    with open("utils/docker/Dockerfile", "w") as dockerfile:
        dockerfile.write(text)