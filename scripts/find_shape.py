#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from opencv_apps.msg import Point2D, Blob, BlobArray, BlobArrayStamped
import cv2
import cv_bridge
import numpy as np

new_blob_available = False
state_stopping = True
state_tracking_blob = True

# NB: change to the x coordinate of the middle point of your screen
x_coord = 320

# get the x coordinate and size of the blob if there is a blob detected
def get_blob(blob_position):
    global new_blob_available, x_coord, size
    if len(blob_position.blobs) > 0 :
        new_blob_available = True
        x_coord = blob_position.blobs[0].center.x
        size = blob_position.blobs[0].radius

def main():
    global new_blob_available, x_coord, size, robot_vel, velocity_pub, state_stopping

    rospy.init_node("find_shape")
    rospy.Subscriber("blob_detection/blobs", BlobArrayStamped, get_blob)

    # NB: change or remap the topic in the publisher
    velocity_pub = rospy.Publisher("mobile_base_controller/cmd_vel", Twist, queue_size=1)
    loop_rate = rospy.Rate(30)

    # spin to the right to find the blobs and stops for 3 seconds when a blob is detected
    # and the detected blob arrives to the middle of the screen
    while not rospy.is_shutdown():
        if state_tracking_blob :
            robot_vel = Twist()
            robot_vel.angular.z = 0.25
            velocity_pub.publish(robot_vel)

            if new_blob_available :
                if x_coord > 320 :
                    state_stopping = True
                if state_stopping :
                    if x_coord < 320 :
                        robot_vel = Twist()
                        robot_vel.angular.z = 0.0
                        velocity_pub.publish(robot_vel)
                        rospy.sleep(3)
                        state_stopping = False

        loop_rate.sleep()

if __name__ == '__main__':
    main()
