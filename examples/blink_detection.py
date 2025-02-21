#!/usr/bin/env python3


# This is a demo of detecting eye status from the users camera. If the users eyes are closed for EYES_CLOSED seconds, the system will start printing out "EYES CLOSED"
# to the terminal until the user presses and holds the spacebar to acknowledge

# this demo must be run with sudo privileges for the keyboard module to work

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# imports
import face_recognition
import cv2
import time
from scipy.spatial import distance as dist  # 用于计算欧几里得距离

EYES_CLOSED_SECONDS = 5

def main():
    closed_count = 0  # 记录连续闭眼的帧数
    video_capture = cv2.VideoCapture(0)  # 打开摄像头，0表示默认摄像头

    # 读取第一帧用于初始化
    ret, frame = video_capture.read(0)
    # cv2.VideoCapture.release()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
      # 将图像缩小到1/4大小以提高处理速度
    # 将BGR格式转换为RGB格式
    rgb_small_frame = small_frame[:, :, ::-1]

    # 获取人脸特征点
    face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)
    # 用于控制每隔一帧处理一次，减少CPU负载
    process = True

    while True:
        # 读取视频帧
        ret, frame = video_capture.read(0)

        # get it into the correct format
        # 图像预处理：缩放和颜色空间转换
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]



        # get the correct face landmarks
        # 每隔一帧处理一次
        if process:
            # 检测人脸特征点
            face_landmarks_list = face_recognition.face_landmarks(rgb_small_frame)

            # get eyes
            for face_landmark in face_landmarks_list:
                # 获取左右眼的特征点
                left_eye = face_landmark['left_eye']
                right_eye = face_landmark['right_eye']

                # 在图像上绘制眼睛区域的矩形
                color = (255,0,0)  # 蓝色
                thickness = 2
                cv2.rectangle(small_frame, left_eye[0], right_eye[-1], color, thickness)

                # 显示处理后的图像
                cv2.imshow('Video', small_frame)

                # 计算左右眼的眼睛纵横比（EAR）
                ear_left = get_ear(left_eye)
                ear_right = get_ear(right_eye)

                # 判断是否闭眼（EAR值小于0.2认为是闭眼）
                closed = ear_left < 0.2 and ear_right < 0.2

                if (closed):
                    closed_count += 1
                else:
                    closed_count = 0

                # 如果连续闭眼时间超过阈值
                if (closed_count >= EYES_CLOSED_SECONDS):
                    asleep = True
                    while (asleep): # 持续循环直到用户确认
                        print("EYES CLOSED")

                        if cv2.waitKey(1) == 32: # 等待空格键按下
                            asleep = False
                            print("EYES OPENED")
                    closed_count = 0

        # 切换处理标志
        process = not process

        # 检测退出键（q键）
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

def get_ear(eye):

    """
    计算眼睛纵横比（Eye Aspect Ratio, EAR）
    EAR = (A + B) / (2.0 * C)
    其中A和B是眼睛垂直方向的两个距离，C是水平方向的距离
    """
    # 计算眼睛垂直方向的两个距离
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates

    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

if __name__ == "__main__":
    main()

