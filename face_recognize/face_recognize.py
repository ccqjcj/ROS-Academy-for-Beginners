import cv2
#人脸检测函数
def face_detect_demo(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#需要根据自己opencv的安装路径来查看xml文件的绝对路径
    face_detector = cv2.CascadeClassifier(r'C:\Users\iCo1in\anaconda3\envs\pytorch\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
    faces = face_detector.detectMultiScale(gray, 1.2, 6)
    # 如果未检测到面部，则返回原始图像
    if (len(faces) == 0):
        return None, None
    # 目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
    (x, y, w, h) = faces[0]
    # 返回图像的脸部部分
    return gray[y:y + w, x:x + h], faces[0]


#导入训练结果
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('train.yml')#读取前文训练的结果


# 根据给定的人脸（x，y）坐标和宽度高度在图像上绘制矩形
def draw_rectangle(img, rect):
    (x, y, w, h) = rect#矩形框
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

# 根据给定的人脸（x，y）坐标写出人名
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (128, 128, 0), 2)

# 此函数识别图像中的人物并在脸部周围绘制一个矩形及其人名
facelabel = ["tanli", "tanli"]#人物名
def predict(image):
    # 生成图像的副本，保留原始图像
    img = image.copy()
    # 检测人脸区域
    face, rect = face_detect_demo(img)#face_detect_demo前面的人脸检测函数
    #print(rect)=[x,y,w,h]
    # 预测人脸名字
    label = recognizer.predict(face)
    print(label)#label[0]为名字，label[1]可信度数值越低，可信度越高（
    if label[1]<=50:
        # 获取由人脸识别器返回的相应标签的人名
        label_text = facelabel[label[0]]

        # 在检测到的脸部周围画一个矩形
        draw_rectangle(img, rect)
        # 标出预测的人名
        draw_text(img, label_text, rect[0], rect[1])
        # 返回预测的图像
        return img
    else:
        # 在检测到的脸部周围画一个矩形
        draw_rectangle(img, rect)
        # 标出预测的人名
        draw_text(img, "not find", rect[0], rect[1])
        # 返回预测的图像
        return img

test_img = cv2.imread(r"E:\face_d\tanli\image1.jpg")
#执行预测
pred_img = predict(test_img)
cv2.imshow('result', pred_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
