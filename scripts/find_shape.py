#!/usr/bin/env python2

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

x_coord = 320


def get_blob(blob_position):
    global new_blob_available, x_coord, size
    if len(blob_position.blobs) > 0 :
        new_blob_available = True
        x_coord = blob_position.blobs[0].center.x
        size = blob_position.blobs[0].radius

def main():
    global new_blob_available, x_coord, size, robot_vel, velocity_pub, state_stopping

    rospy.init_node("blob_follower")
    rospy.Subscriber("blob_detection/blobs", BlobArrayStamped, get_blob)
   
    velocity_pub = rospy.Publisher("mobile_base_controller/cmd_vel", Twist, queue_size=1)
    loop_rate = rospy.Rate(30)

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