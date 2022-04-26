#!/usr/bin/env python2

import rospy
from geometry_msgs.msg import Point, Twist
from std_msgs.msg import Int32
from blob_detector.msg import blob
import cv2
import cv_bridge
from sensor_msgs.msg import Image
import numpy as np



new_blob_available = False

x_coord = 400
size = 120 



def get_blob(blob_position):
    global new_blob_available, x_coord, size
    new_blob_available = True
    x_coord = blob_position.position.x
    size = blob_position.size       



def main():
    global new_blob_available, x_coord, size, robot_vel, velocity_pub

   
    rospy.init_node("blob_follower_with_angz")
    
    
    rospy.Subscriber("blob_location", blob, get_blob)
   
    velocity_pub = rospy.Publisher("robotont/cmd_vel", Twist, queue_size=1)

    
    while not rospy.is_shutdown():
        if new_blob_available :
            robot_vel = Twist()
            if x_coord < 400 :
               # robot_vel.linear.y = 0.1
                robot_vel.angular.z = 0.15
            elif x_coord > 400 :
               # robot_vel.linear.y = -0.1
                robot_vel.angular.z = -0.15          
            else:
                #robot_vel.linear.y = 0.0
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

   
