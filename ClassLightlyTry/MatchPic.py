import cv2
from matplotlib import pyplot as plt

template = cv2.imread("images/Mat01.jpg", 1)  # 读取模板图像
if template is None:
    print("无法读取模板图像")
    exit()
target = cv2.imread("images/Mat02.jpg", 1)  # 读取目标图像
if target is None:
    print("无法读取目标图像")
    exit()
# 建立ORB特征检测器
orb = cv2.ORB_create(
    nfeatures=500,
    scaleFactor=1.2,
    nlevels=8,
    edgeThreshold=20,
    firstLevel=0,
    WTA_K=2,
    patchSize=20,
    fastThreshold=20,
)
kp1, des1 = orb.detectAndCompute(template, None)  # 计算template中的特征点和描述符
kp2, des2 = orb.detectAndCompute(target, None)  # 计算target中的特征点和描述符
# 建立配准关系
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
mathces = bf.match(des1, des2)  # 配准描述符
mathces = sorted(mathces, key=lambda x: x.distance)  # 依据距离排序
# 画出配准关系
result = cv2.drawMatches(template, kp1, target, kp2, mathces[:40], None, flags=2)
plt.imshow(result), plt.show()
