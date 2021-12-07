import os
import numpy as np
import cv2

#脸部检测函数
def face_detect_demo(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_detector = cv2.CascadeClassifier(r'C:\Users\iCo1in\anaconda3\envs\pytorch\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(gray, 1.2, 6)
    # 如果未检测到面部，则返回原始图像
    if (len(faces) == 0):
        return None, None
    # 目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
    (x, y, w, h) = faces[0]
    # 返回图像的脸部部分
    return gray[y:y + w, x:x + h], faces[0]

def ReFileName(dirPath):
    """
    :param dirPath: 文件夹路径
    :return:
    """
    # 对目录下的文件进行遍历
    faces=[]
    for file in os.listdir(dirPath):
        # 判断是否是文件
        if os.path.isfile(os.path.join(dirPath, file)) == True:
           c= os.path.basename(file)
           name = dirPath + '\\' + c
           img = cv2.imread(name)
           # 检测脸部
           face, rect = face_detect_demo(img)
           # 我们忽略未检测到的脸部
           if face is not None:
               # 将脸添加到脸部列表并添加相应的标签
               faces.append(face)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces

#tanli照片读取（同学1）
dirPathtanli = r"E:\face_d\tanli"#文件路径
tanli=ReFileName(dirPathtanli)#调用函数

labeltanli=np.array([0 for i in range(len(tanli))])#标签处理
#wangqin照片读取（同学2）
dirPathtanli = r"E:\face_d\tanli"#文件路径
tanli=ReFileName(dirPathtanli)#调用函数
labeltanli=np.array([1 for i in range(len(tanli))])#标签处理

#拼接并打乱数据特征和标签
x=np.concatenate((tanli,tanli),axis=0)
y=np.concatenate((labeltanli,labeltanli),axis=0)

index = [i for i in range(len(y))] # test_data为测试数据
np.random.seed(1)
np.random.shuffle(index) # 打乱索引
train_data = x[index]
train_label = y[index]

#分类器
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(train_data, train_label)
# 保存训练数据
recognizer.write(r'E:\face_d\train.yml')
