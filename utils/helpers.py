import logging
import os

import fs_s3fs
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

current_env = os.getenv('OS_ENV', 'OSX').lower()

s3fs = fs_s3fs.S3FS(
    bucket_name=os.getenv('S3_BUCKET_NAME'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID_'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY_'),
    dir_path=f'{os.getenv("APP_NAME")}/'
)

paths = {
    'cookies': f'cookies/{current_env}',
    'screenshots': 'debug-screenshots',
}
for path in paths.values():
    path_dirs = path.split('/')
    for i in range(len(path_dirs)):
        if not s3fs.exists('/'.join(path_dirs[:i + 1])):
            s3fs.makedir('/'.join(path_dirs[:i + 1]))
