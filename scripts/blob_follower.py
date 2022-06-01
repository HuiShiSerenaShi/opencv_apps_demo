#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from opencv_apps.msg import Point2D, Blob, BlobArray, BlobArrayStamped
import cv2
import cv_bridge
import numpy as np

new_blob_available = False

# NB: change to the x coordinate of the middle point of your screen
x_coord = 320
size = 170 

# get the x coordinate and size of the blob if there is a blob detected
def get_blob(blob_position):
    global new_blob_available, x_coord, size
    if len(blob_position.blobs) > 0 :
        new_blob_available = True
        x_coord = blob_position.blobs[0].center.x
        size = blob_position.blobs[0].radius

def main():
    global new_blob_available, x_coord, size, robot_vel, velocity_pub

    rospy.init_node("blob_follower")
    rospy.Subscriber("blob_detection/blobs", BlobArrayStamped, get_blob)

    # NB: change or remap the topic in the publisher
    velocity_pub = rospy.Publisher("mobile_base_controller/cmd_vel", Twist, queue_size=1)
    loop_rate = rospy.Rate(30)

    # The robot spins to the right to find the blob and follows the blob if it is detected.
    # When following, the robot checks if the blob is at the middle of the screen
    # to decide turn right or left, and it checks the size of the blob
    # to decide going forward or backward.
    # When a blob is out of the field of view of the robot camera,
    # the robot spins to the right to look for the blob.
    while not rospy.is_shutdown():
        if new_blob_available :
            robot_vel = Twist()
            if x_coord < 320 :
                robot_vel.angular.z = 0.15
            elif x_coord > 320 :
                robot_vel.angular.z = -0.15
            else:
                robot_vel.angular.z = 0.0

            if size < 170:
                robot_vel.linear.x = 0.3
            elif size > 170:
                robot_vel.linear.x = -0.3
            else:
                robot_vel.linear.x = 0.0

            velocity_pub.publish(robot_vel)
            new_blob_available = False

        else :
            robot_vel = Twist()
            robot_vel.angular.z = 0.15
            velocity_pub.publish(robot_vel)

        loop_rate.sleep()

if __name__ == '__main__':
    main()
