import cv2

# Đọc ảnh
image = cv2.imread("image/circle.jpg")

# Chuyển đổi sang ảnh xám
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng Canny Edge Detection để xác định đường viền
edges = cv2.Canny(gray, 50, 150)

# Tìm các đường viền
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Lọc các đường viền không phù hợp (tùy chọn)
filtered_contours = []
min_contour_area = 1000  # Diện tích tối thiểu
for contour in contours:
    area = cv2.contourArea(contour)
    if area > min_contour_area:
        filtered_contours.append(contour)

# Vẽ bounding box cho mỗi đường viền
for contour in filtered_contours:
    # Tìm tọa độ và kích thước của bounding box
    x, y, w, h = cv2.boundingRect(contour)
    # Vẽ bounding box lên ảnh gốc
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Hiển thị ảnh gốc với bounding box
cv2.imshow("Image with Bounding Box", image)
cv2.waitKey(0)
cv2.destroyAllWindows()