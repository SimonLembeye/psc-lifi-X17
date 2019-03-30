#!/usr/bin/env python

import rospy
import sys
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2

def newOdom(msg):
	global x, y, theta
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y

	rot_q = msg.pose.pose.orientation
	theta = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])[2]

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

err = """
Communications Failed or Error Compilation
"""

def info(linear_vel, angular_vel, pos):
    return "currently:\tlinear vel %s\t angular vel %s\t pos %s " % (linear_vel, angular_vel, pos)

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input
    return input

def checkLinearLimitVelocity(vel):
    vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    return vel

def checkAngularLimitVelocity(vel):
    vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    return vel

x = 0.0
y = 0.0
theta = 0.0

rospy.init_node("turtlebot3_goal", anonymous=True)
sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

twist = Twist()
twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0

r = rospy.Rate(10)

goal = Point()
goal.x = 0.0
goal.y = 0.0

twist = Twist()

while not rospy.is_shutdown():
	inc_x = goal.x - x
	inc_y = goal.y - y
	inc_theta = atan2(inc_y, inc_x) - theta

	print "Position: (%.3f, %.3f)\tAngle: %.1f\tMove: (%.3f, %.3f)\tTurn: %.1f" % (x, y, theta*180/3.1415, inc_x, inc_y, inc_theta*180/3.1415)

	if abs(inc_theta) > 0.1:
		twist.linear.x = 0.0
		twist.angular.z = 0.3
	else:
		twist.linear.x = 0.5
		twist.angular.z = 0.0

	pub.publish(twist)
	r.sleep()

twist = Twist()
twist.linear.x = 0.0
twist.angular.z = 0.0
pub.publish(twist)
