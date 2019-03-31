#!/usr/bin/env python

import rospy
import sys
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

err = """
Communications Failed or Error Compilation
"""

def newOdom(msg):
	global x, y, theta
	x = msg.pose.pose.position.x
	y = msg.pose.pose.position.y

	rot_q = msg.pose.pose.orientation
	theta = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])[2]

def info(pos_x, pos_y, inc_x, inc_y, inc_theta):
    return "Pos: (%.3f, %.3f)\tMove: (%.3f, %.3f)\tTurn: %3.1f" % (pos_x, pos_y, inc_x, inc_y, inc_theta*180/3.1415)

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

LIN_VEL = checkLinearLimitVelocity(0.2)
ANG_VEL = checkAngularLimitVelocity(0.5)

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
sys.stdout.write("Provide goal.x: ")
goal.x = input()
sys.stdout.write("Provide goal.y: ")
goal.y = input()

twist = Twist()

while not rospy.is_shutdown():
	inc_x = goal.x - x
	inc_y = goal.y - y
	inc_theta = atan2(inc_y, inc_x) - theta
	if inc_theta > 3.14:
		inc_theta -= 6.28
	if inc_theta < -3.14:
		inc_theta += 6.28

	if abs(inc_x) < 0.01 and abs(inc_y) < 0.01:
		twist = Twist()
		twist.linear.x = 0.0
		twist.angular.z = 0.0
		pub.publish(twist)
		print info(x, y, inc_x, inc_y, inc_theta)
		print "\nYour robot has arrived at its destination (%.2f, %.2f) with error of (%.3f, %.3f)" % (goal.x, goal.y, inc_x, inc_y)
		sys.exit()

	print info(x, y, inc_x, inc_y, inc_theta)

	if abs(inc_theta) > 0.1:
		twist.linear.x = 0.0
		if inc_theta < 0:
			twist.angular.z = -ANG_VEL
		else:
			twist.angular.z = ANG_VEL
	else:
		twist.linear.x = LIN_VEL
		twist.angular.z = 0.0

	pub.publish(twist)
	r.sleep()