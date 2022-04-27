#!/usr/bin/env python2

import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from opencv_apps.msg import Point2D, Blob, BlobArray, BlobArrayStamped
import cv2
import cv_bridge
import numpy as np

new_blob_available = False

x_coord = 400
size = 120 

def get_blob(blob_position):
    global new_blob_available, x_coord, size
    if len(blob_position.blobs) > 0 :
        new_blob_available = True
        x_coord = blob_position.blobs[0].center.x
        size = blob_position.blob_position.blobs[0].radius

def main():
    global new_blob_available, x_coord, size, robot_vel, velocity_pub

    rospy.init_node("blob_follower")
    rospy.Subscriber("blobs", BlobArrayStamped, get_blob)
   
    velocity_pub = rospy.Publisher("mobile_base_controller/cmd_vel", Twist, queue_size=1)

    while not rospy.is_shutdown():
        if new_blob_available :
            robot_vel = Twist()
            if x_coord < 400 :
                robot_vel.angular.z = 0.15
            elif x_coord > 400 :
                robot_vel.angular.z = -0.15
            else:
                robot_vel.angular.z = 0.0

            if size < 120:
                robot_vel.linear.x = 0.1 
            elif size > 120:
                robot_vel.linear.x = -0.1
            else:
                robot_vel.linear.x = 0.0

            velocity_pub.publish(robot_vel)

            new_blob_available = False


if __name__ == '__main__':
    main()
