import os
import httpx
import loguru

CAST_SERVICE_HOST_URL = 'http://localhost:8002/api/v1/casts/'
url = os.environ.get('CAST_SERVICE_HOST_URL', CAST_SERVICE_HOST_URL)


def is_cast_present(cast_id: int):
    r = httpx.get(f'{url}{cast_id}/')
    loguru.logger.info(r.json())
    return True if r.status_code == 200 else False
