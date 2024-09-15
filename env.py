import os

SECRET          = os.environ.get('SECRET','33cc366e9e6b04c0adfab849979d7e8409c7e2b35986cba1')
ALGORITHM       = os.environ.get('ALGORITHM','HS256')
IMAGES_NAME     = os.environ.get('IMAGES_NAME','build-test')
SQL             = os.environ.get('SQL','postgresql://postgres:admin@localhost:5432/virtualweb')

USER_API        = os.environ.get('USER_API','http://localhost:8000/api')
MANAGEMENT_API  = os.environ.get('MANAGEMENT_API','http://localhost:8001/api')
CONTAINER_API   = os.environ.get('CONTAINER_API','http://localhost:8002/api')
WHITELIST_API   = os.environ.get('WHITELIST_API','http://localhost:8003/api')
DOCKER_CLIENT   = os.environ.get('DOCKER_CLIENT','tcp://127.0.0.1:2375')