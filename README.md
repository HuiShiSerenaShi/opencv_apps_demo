# opencv_apps_demo

Blob Detection Demo:

Running Steps:

NB: Checkout the blob_detection_nodelet branch of opencv_apps.
Replace "YourTopic" in the following command to the actual image topic.

Find Shape:

roslaunch opencv_apps blob_detection.launch image:=YourTopic

rosrun opencv_apps_demo find_shape.py


Blob Follower:

roslaunch opencv_apps blob_detection.launch image:=YourTopic

rosrun opencv_apps_demo blob_follower.py


Demo Video Link:

https://www.youtube.com/watch?v=CJXP0X5rQqs

