import face_recognition
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
from pathlib import Path

class MultiFaceCheckInSystem:
    def __init__(self):
        # 存储已知人脸的编码和对应的人员信息
        self.known_face_encodings = []
        self.known_face_names = []
        # 签到记录
        self.attendance_records = []

    def register_person(self, name, image_path):
        """注册人员到系统"""
        try:
            # 加载图片并提取人脸编码
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]

            # 保存人脸编码和对应姓名
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)
            print(f"成功注册 {name}")
            return True
        except Exception as e:
            print(f"注册失败: {str(e)}")
            return False

    def process_image(self, image_path):
        """处理单张图片进行多人签到"""
        # 加载图片
        image = face_recognition.load_image_file(image_path)

        # 获取图片中所有人脸的位置和编码
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # 用于存储当前图片中识别到的人员
        detected_people = []

        # 处理每个检测到的人脸
        for face_encoding in face_encodings:
            # 将当前人脸与所有已知人脸比较
            matches = face_recognition.compare_faces(
                self.known_face_encodings,
                face_encoding,
                tolerance=0.6  # 可调整阈值
            )

            # 如果找到匹配
            if True in matches:
                # 获取匹配的人员姓名
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                detected_people.append(name)

                # 记录签到
                self._record_attendance(name)

        return detected_people

    def process_video(self):
        """处理视频流进行多人签到"""
        video_capture = cv2.VideoCapture(0)

        # 用于防止重复签到
        processed_names = set()

        while True:
            ret, frame = video_capture.read()

            # 降低分辨率以提高性能
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            # 获取当前帧中所有人脸的位置和编码
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            # 在图像上标记人脸
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # 将人脸与已知人脸比较
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding
                )

                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                    # 如果这个人还没有签到
                    if name not in processed_names:
                        self._record_attendance(name)
                        processed_names.add(name)

                # 还原到原始图像大小
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # 在图像上绘制框和名字
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # 显示结果
            cv2.imshow('Video', frame)

            # 按'q'退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def _record_attendance(self, name):
        """记录签到信息"""
        now = datetime.now()
        record = {
            'name': name,
            'time': now.strftime('%Y-%m-%d %H:%M:%S')
        }
        self.attendance_records.append(record)
        print(f"{name} 签到成功！时间：{record['time']}")

    def export_attendance(self, filename='attendance.csv'):
        """导出签到记录"""
        df = pd.DataFrame(self.attendance_records)
        df.to_csv(filename, index=False)
        print(f"签到记录已导出到 {filename}")

# 使用示例
if __name__ == "__main__":
    # 创建签到系统实例
    system = MultiFaceCheckInSystem()

    # 注册人员（实际使用时需要替换为真实图片路径）
    base_dir = Path("E:/Acodes/git/face_recognition-edu/checkin/pics")
    system.register_person("胡歌", str(base_dir / "HuGe.jpg"))
    system.register_person("周杰伦", str(base_dir / "JayChou.jpg"))
    # system.register_person("彦祖", str(base_dir / "YZ.jpg"))
    system.register_person("彦祖", str(base_dir / "YZ_test.jpg"))
    # 方式1：处理单张图片
    detected = system.process_image(str(base_dir /"HuGe_test2.jpg"))
    # detected2 = system.process_image(str(base_dir / "YZ_test.jpg"))
    detected2 = system.process_image(str(base_dir / "YZ.jpg"))
    detected3 = system.process_image(str(base_dir / "HuGe_test1.jpg"))
    detected4 = system.process_image(str(base_dir / "biden.jpg"))
    detected5 = system.process_image(str(base_dir / "YZ_test2.jpg"))
    print(f"检测到的人员：{detected}")
    print(f"检测到的人员：{detected2}")
    print(f"检测到的人员：{detected3}")
    print(f"检测到的人员：{detected4}")
    print(f"检测到的人员：{detected5}")
    #
    # # 方式2：处理视频流
    # system.process_video()
    #
    # # 导出签到记录
    # system.export_attendance()
