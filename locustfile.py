import io
from locust import HttpUser, task
from PIL import Image
from pathlib import Path

class QuickstartUser(HttpUser):
    host = "http://localhost:9000" 

    @task
    def main_route(self):
        self.client.get("/")

    @task
    def send_images(self):
        image_path = Path("test_images") / "3" / "Sign 3 (30).jpeg"
        img = Image.open(image_path)

        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='JPEG')
        img_byte_array.seek(0)

        imgData = {
            "file": ("Sign 3 (30).jpeg", img_byte_array, "image/jpeg")
        }

        self.client.post("/prediction", files=imgData)
