from requests_toolbelt.multipart.encoder import MultipartEncoder 
from fastapi import FastAPI, UploadFile, File, HTTPException 
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse 
import function
import string
import uuid 
import cv2 
import os
import io

# khởi tạo một đối tượng FastAPI 
app = FastAPI() 
# url file ảnh 
image_path_file = 'image/' 

# in ra hình ảnh 
@app.get("/get_image/{file_name}") 
async def get_image(file_name: str): 
    img_path = f"{image_path_file}{file_name}" 
    if not os.path.exists(img_path): 
        raise HTTPException(status_code=404, detail="không tìm thấy file ảnh, check url") 
    return FileResponse(img_path, media_type="image/jpeg") 

# thêm ảnh màu 
@app.post("/create_upload_file") 
async def create_upload_file(file: UploadFile = File(...)): 
    file.filename = f"{uuid.uuid4()}.jpg" 
    contents = await file.read() 
    with open(f"{image_path_file}{file.filename}", "wb") as f: 
        f.write(contents) 
    return {"filename": file.filename} 

# thêm và đổi thành ảnh đen trắng ___lưu lên local___
@app.post("/convert_grays_color")
async def convert_grays_color(file: UploadFile = File(...)): 
    # Đọc file ảnh 
    contents = await file.read() 
     
    # Tạo tên tệp duy nhất 
    # filename = f"{uuid.uuid4()}.jpg" 
    filename = os.path.basename(function.generate_filename()) + ".jpg"
    
    # Lưu ảnh tải lên 
    with open(f"{image_path_file}{filename}", "wb") as f: 
        f.write(contents) 
     
    # Đọc hình ảnh đã lưu 
    img_path = f"{image_path_file}{filename}" 
    RGB_img = cv2.imread(img_path) 
     
    # Đổi qua màu đen trắng 
    gray_img = cv2.cvtColor(RGB_img, cv2.COLOR_BGR2GRAY) 
     
    # Lưu ảnh đen trắng 
    gray_filename = f"gray_{filename}" 
    gray_img_path = f"{image_path_file}{gray_filename}"    
    cv2.imwrite(gray_img_path, gray_img) 
     
    # Trả về 
    return FileResponse(gray_img_path, media_type="image/jpeg")


# thêm ảnh đen trắng mà ___không lưu ảnh lên local___

@app.post("/convert_grays_color_dont_save_local")
async def convert_grayscale_dont_save_local(file: UploadFile = File(...)):
    # Đọc nội dung của tệp
    contents = await file.read()

    # Xử lý tên tệp
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    file_name = "".join(c for c in file.filename if c in valid_chars)

    # Chuyển đổi ảnh thành đen trắng
    grayscale_image = await function.convert_to_grayscale(contents)

    # Trả về ảnh đen trắng dưới dạng phản hồi luồng
    return StreamingResponse(io.BytesIO(grayscale_image), media_type="image/jpeg", headers={"Content-Disposition": f"attachment; filename={file_name}"})


# xoá 
@app.delete("/delete_image/{file_name}") 
async def delete_image(file_name: str): 
    img_path = f"{image_path_file}{file_name}" 
    if os.path.exists(img_path): 
        os.remove(img_path) 
        return {"message": f"xoá ảnh '{file_name}' thành công"} 
    else: 
        raise HTTPException(status_code=404, detail="không tìm thấy file ảnh, check url") 
 
# đổi port 
if __name__ == "__main__": 
    import uvicorn 
    uvicorn.run(app, host="127.0.0.1", port=8000) 
 
# Tạo API có chức năng học và hiển thị ảnh 
# Request: ảnh (png / jpg/ bmp / ...) => có thể gửi trực tiếp từ postman / tạo script python gửi ảnh 
# API: Cứ có request => đọc ảnh và chuyển ảnh về dạng đen trắng (gray) => hiển thị ảnh (dùng thư viện opencv)