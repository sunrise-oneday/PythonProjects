import cv2
import os

# 图片路径（请确认实际路径）
image_path = r'C:\Users\77496\Pictures\ENDFIELD\ENDFIELD_SHARE_1771121191.png'

# 检查文件是否存在
if not os.path.exists(image_path):
    print("错误：文件不存在，请检查路径")
    exit()

# 读取图像
img = cv2.imread(image_path, cv2.IMREAD_COLOR)  # 使用枚举值更清晰
if img is None:
    print("错误：无法读取图像，文件可能已损坏")
    exit()

# 显示图像
cv2.imshow('SATOMI', img)
print("图像已显示，按任意键关闭窗口")

# 等待按键并关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()