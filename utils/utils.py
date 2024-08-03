def change_dockerfile(text: str):
    # ret_text = ""

    with open("utils/docker/Dockerfile", "w") as dockerfile:
        dockerfile.write(text)
    
    # with open("utils/docker/Dockerfile", "r") as dockerfile:
    #     ret_text = dockerfile.read()
    
    # return ret_text