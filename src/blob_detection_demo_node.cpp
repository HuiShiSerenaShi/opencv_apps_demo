#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "opencv_apps/BlobArrayStamped.h"

ros::Subscriber blobs_sub;
ros::Publisher velocity_pub;
opencv_apps::BlobArrayStamped new_blobs_msg;
geometry_msgs::Twist robot_vel;

int frame_width = 640;
float angular_speed_z = 1.5;

void rotateAroundZ(float angular_speed_z)
{
        robot_vel.linear.x = 0;
        robot_vel.linear.y = 0;
        robot_vel.angular.z = angular_speed_z;
        velocity_pub.publish(robot_vel);
}

void stop()
{
    robot_vel.linear.x = 0;
    robot_vel.linear.y = 0;
    robot_vel.angular.z = 0;
    velocity_pub.publish(robot_vel);
}


void getBlobs(opencv_apps::BlobArrayStamped blobs_msg)
{
   new_blobs_msg = blobs_msg;
}

int main(int argc, char **argv)

{
  ros::init(argc, argv, "blob_detection_demo_node");
  ros::NodeHandle nh;
  velocity_pub = nh.advertise<geometry_msgs::Twist>("cmd_vel", 1);
  blobs_sub = nh.subscribe("blob_detection/blobs", 1000, getBlobs);

  if (new_blobs_msg.blobs[0].center.x < frame_width/2)
  {
    stop();
    ros::Duration(1).sleep();
  }

  else
  {
    rotateAroundZ(angular_speed_z);
  }


//    ---
// header: 
//   seq: 6575
//   stamp: 
//     secs: 1643376036
//     nsecs: 417656421
//   frame_id: "usb_cam"
// blobs: 
//   - 
//     center: 
//       x: 547.918273926
//       y: 381.227722168
//     radius: 128.778198242
//   - 
//     center: 
//       x: 405.204101562
//       y: 108.691574097
//     radius: 420.648895264
// ---

  ros::spin();

  return 0;
}