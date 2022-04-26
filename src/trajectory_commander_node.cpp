#include "ros/ros.h"
#include "geometry_msgs/Twist.h"


geometry_msgs::Twist robot_vel;
ros::Publisher velocity_pub;

void driveAlongX(float linx_value, int duration)
{   

    for (int i = 0; i < duration; i++)
    {
        robot_vel.linear.x = linx_value;
        robot_vel.linear.y = 0.0;
        robot_vel.angular.z = 0.0;
        velocity_pub.publish(robot_vel);
        ros::Duration(0.1).sleep();
    }
}

void driveAlongY(float liny_value, int duration)
{   

    for (int i = 0; i < duration; i++)
    {
        robot_vel.linear.x = 0;
        robot_vel.linear.y = liny_value;
        robot_vel.angular.z = 0.0;
        velocity_pub.publish(robot_vel);
        ros::Duration(0.1).sleep();
    }
}

void rotateAroundZ(float angz_value, int duration)
{   

    for (int i = 0; i < duration; i++)
    {
        robot_vel.linear.x = 0;
        robot_vel.linear.y = 0;
        robot_vel.angular.z = angz_value;
        velocity_pub.publish(robot_vel);
        ros::Duration(0.1).sleep();
    }
}

void rotateAndForward(float linx_value, float angz_value, int duration)
{   

    for (int i = 0; i < duration; i++)
    {
        robot_vel.linear.x = linx_value;
        robot_vel.linear.y = 0;
        robot_vel.angular.z = angz_value;
        velocity_pub.publish(robot_vel);
        ros::Duration(0.1).sleep();
    }
}

void stop()
{   

    robot_vel.linear.x = 0;
    robot_vel.linear.y = 0;
    robot_vel.angular.z = 0;
    velocity_pub.publish(robot_vel);
    
}

void circle(float linx_value, float angz_value, int duration)
{   

    for (int i = 0; i < duration; i++)
    {
        robot_vel.linear.x = linx_value;
        robot_vel.linear.y = 0;
        robot_vel.angular.z = angz_value;
        velocity_pub.publish(robot_vel);
        ros::Duration(0.1).sleep();
    }
}

void simpleSquare()
{   
    driveAlongX(0.1, 30);
    stop();
    driveAlongY(-0.1, 30);
    stop();
    driveAlongX(-0.1, 30);
    stop();
    driveAlongY(0.1, 30);
    stop();
}

void nonHolonomicSquare()
{   
    rotateAroundZ(1.57079637, 10);
    stop();
    driveAlongX(0.1, 30);
    stop();
    rotateAroundZ(1.57079637, 10);
    stop();
    driveAlongX(0.1, 30);
    stop();
    rotateAroundZ(1.57079637, 10);
    stop();
    driveAlongX(0.1, 30);
    stop();
    rotateAroundZ(1.57079637, 10);
    stop();
    driveAlongX(0.1, 30);
    stop();
}

void infinity()
{   
    rotateAndForward(0.1, 1.57079637, 30);
    stop();
        
    driveAlongX(0.1, 19);
    stop();

    rotateAndForward(0.1, -1.57079637, 30);
    stop();
        
    driveAlongX(0.1, 19);
    stop();

}


int main(int argc, char **argv)

{
  ros::init(argc, argv, "trajectory_commander_node");
  ros::NodeHandle n;
  velocity_pub =
    n.advertise<geometry_msgs::Twist>("mobile_base_controller/cmd_vel", 1);
  
  ros::Rate loop_rate(10);

  while (ros::ok())
  {
      //Each shape will run twice, then change to the next shape.
      simpleSquare();
      simpleSquare();
      nonHolonomicSquare();
      nonHolonomicSquare();
      circle(0.1, 0.5235988, 120);
      circle(0.1, 0.5235988, 120);
      infinity();
      infinity();

      loop_rate.sleep();
  }

  return 0;
}
