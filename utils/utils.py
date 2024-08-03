from utils.jwt.jwt_utils import decode_jwt

def check_role(id: str):
    if id == "10":
        return "ADMIN"
    elif id == "20":
        return "USER"
    else:
        return "NO ROLE"

def check_admin_role(token: str):
    decoded_token = decode_jwt(token)
    return check_role(str(decoded_token["user_id"])[:2]) == "ADMIN"

def check_user_role(token: str):
    decoded_token = decode_jwt(token)
    return check_role(str(decoded_token["user_id"])[:2]) == "USER"

def change_dockerfile(text: str):
    # ret_text = ""

    with open("utils/docker/Dockerfile", "w") as dockerfile:
        dockerfile.write(text)
    
    # with open("utils/docker/Dockerfile", "r") as dockerfile:
    #     ret_text = dockerfile.read()
    
    # return ret_text