=====
Usage
=====

To use Face Recognition in a project::

    import face_recognition

See the examples in the /examples folder on github for how to use each function.

You can also check the API docs for the 'face_recognition' module to see the possible parameters for each function.

The basic idea is that first you load an image::

    import face_recognition

    image = face_recognition.load_image_file("your_file.jpg")

That loads the image into a numpy array. If you already have an image in a numpy array, you can skip this step.

Then you can perform operations on the image, like finding faces, identifying facial features or finding face encodings::

    # Find all the faces in the image
    face_locations = face_recognition.face_locations(image)

    # Or maybe find the facial features in the image
    face_landmarks_list = face_recognition.face_landmarks(image)

    # Or you could get face encodings for each face in the image:
    list_of_face_encodings = face_recognition.face_encodings(image)

Face encodings can be compared against each other to see if the faces are a match. Note: Finding the encoding for a face
is a bit slow, so you might want to save the results for each image in a database or cache if you need to refer back to
it later.

But once you have the encodings for faces, you can compare them like this::

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_face_encodings, a_single_unknown_face_encoding)

It's that simple! Check out the examples for more details.
中文使用说明
===========

如何在项目中使用人脸识别
--------------------

首先导入 face_recognition 库::

    import face_recognition

加载图片::

    image = face_recognition.load_image_file("你的图片.jpg")

这会将图片加载为 numpy 数组。如果你已经有了 numpy 数组格式的图片，可以跳过这一步。

然后你可以对图片进行各种操作，比如：

1. 查找人脸位置::

    # 查找图片中所有的人脸
    face_locations = face_recognition.face_locations(image)

2. 识别面部特征::

    # 获取图片中的面部特征点
    face_landmarks_list = face_recognition.face_landmarks(image)

3. 获取人脸编码::

    # 获取图片中每个人脸的特征编码
    list_of_face_encodings = face_recognition.face_encodings(image)

人脸特征编码可以用来比较不同的人脸是否匹配。注意：获取人脸编码的过程相对较慢，如果需要反复使用同一张脸的编码，建议将结果保存到数据库或缓存中。

比较人脸示例::

    # results 是一个布尔值数组，表示未知人脸是否与已知人脸数组中的任何一个匹配
    results = face_recognition.compare_faces(known_face_encodings, a_single_unknown_face_encoding)

使用建议
-------

1. 对于实时视频处理，建议降低图片分辨率以提高性能
2. 可以通过调整 face_locations() 的 model 参数在速度和准确度之间取得平衡
3. 对于大规模人脸识别，建议使用 GPU 加速

更多示例请查看 GitHub 仓库中的 /examples 文件夹。