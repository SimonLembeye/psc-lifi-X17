#!/usr/bin/env python

import rospy
import sys
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2, pi

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

def shut_down():
	print("\n####################End of execution####################\n")
	twist = Twist()
	twist.linear.x = 0.0
	twist.angular.z = 0.0
	pub.publish(twist)

def print_info(pos_x, pos_y, theta, inc_theta):
    print "Pos: (%.3f, %.3f)\tAng: %3.1f\tTurn: %3.1f" % (pos_x, pos_y, theta*180/pi, inc_theta*180/pi)

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

def betweenMinusPiAndPi(theta):
    res = divmod(theta, 2*pi)[1]
    if res > pi:
        res -= 2*pi
    return res

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

rospy.on_shutdown(shut_down)

while not rospy.is_shutdown():
	inc_x = goal.x - x
	inc_y = goal.y - y
	inc_theta = betweenMinusPiAndPi(atan2(inc_y, inc_x) - theta)

	if abs(inc_x) < 0.01 and abs(inc_y) < 0.01:
		twist.linear.x = 0.0
		twist.angular.z = 0.0
		pub.publish(twist)
		print_info(x, y, theta, inc_theta)
		print "\nYour robot has arrived at its destination (%.2f, %.2f) with error of (%.3f, %.3f)" % (goal.x, goal.y, inc_x, inc_y)
		sys.exit()

	print_info(x, y, theta, inc_theta)

	if abs(inc_theta) > 0.05:
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