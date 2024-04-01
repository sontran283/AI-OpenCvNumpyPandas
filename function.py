import cv2
import numpy as np
import tempfile 
import os

image_path_file = 'image/' 

# Chuyển đổi ảnh thành đen trắng mà không lưu ảnh lên local
async def convert_to_grayscale(contents: bytes) -> bytes:
    # Đọc ảnh từ nội dung được cung cấp
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    filename = os.path.basename(generate_filename()) + ".jpg"

    # Chuyển đổi ảnh sang đen trắng
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray_filename = f"gray_{filename}" 
    gray_img_path = f"{image_path_file}{gray_filename}"    
    cv2.imwrite(gray_img_path, gray_img)

    # Chuyển ảnh đen trắng thành nội dung bytes
    _, img_encoded = cv2.imencode('.jpg', gray_img)
    return img_encoded.tobytes()


# Hàm random tạo tên tệp
def generate_filename() -> str:
    return tempfile.NamedTemporaryFile().name