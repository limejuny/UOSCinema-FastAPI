# import json
# import os

# from os import path
from app.common.config import get_secret

# base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))

# secret_file = os.path.join(base_dir, 'app/common/secrets.json')
JWT_SECRET = get_secret('JWT_SECRET')
JWT_ALGORITHM = "HS256"
