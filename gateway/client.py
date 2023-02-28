import os
import httpx


auth_client = httpx.Client(base_url=f"http://{os.environ.get('AUTH_SERVICE_NAME')}:8000")
