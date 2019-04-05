#!/usr/bin/env python

import rospy
import sys
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point
from geometry_msgs.msg import Twist
from math import atan2, cos, sin, pi

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
    if pos_x is None or pos_y is None or theta is None:
        print "Suscribing..."
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

def finish_suscribe():
    global x, y, theta
    if x is None:
        return False
    if y is None:
        return False
    if theta is None:
        return False
    return True

def goal(goal_x, goal_y):
    global x, y, theta
    goal = Point()
    goal.x = goal_x
    goal.y = goal_y

    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0

    while not rospy.is_shutdown():
        inc_x = goal.x - x
        inc_y = goal.y - y
        inc_theta = betweenMinusPiAndPi(atan2(inc_y, inc_x) - theta)

        if abs(inc_x) < 0.01 and abs(inc_y) < 0.01:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            pub.publish(twist)
            print_info(x, y, theta, inc_theta)
            return

        print_info(x, y, theta, inc_theta)

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
        rate.sleep()

def turn(ang):
    global x, y, theta
    
    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    
    while not finish_suscribe():
        pub.publish(twist)

    theta0 = theta
    ang_rad = betweenMinusPiAndPi(ang*pi/180)

    if ang_rad > 0:
        twist.angular.z = -ANG_VEL
    else:
        twist.angular.z = ANG_VEL
    pub.publish(twist)

    while not rospy.is_shutdown():
        inc_theta = betweenMinusPiAndPi(theta + ang_rad - theta0)
        if abs(inc_theta) < 0.05:
            twist.angular.z = 0.0
            pub.publish(twist)
            print_info(x, y, theta, inc_theta)
            return
        print_info(x, y, theta, inc_theta)
        pub.publish(twist)
        rate.sleep()

def left_turn(ang):
    print "\n####################Turning left####################"
    print "Turn: %3.1f deg\n" % ang
    turn(ang)

def right_turn(ang):
    print "\n####################Turning right####################"
    print "Turn: %3.1f deg\n" % ang
    turn(-ang)

def strait(dis):
    global x, y, theta
    
    twist = Twist()
    twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
    
    while not finish_suscribe():
        pub.publish(twist)

    goal_x = x + dis*cos(theta)
    goal_y = y + dis*sin(theta)
    theta0 = theta
    print "goal: (%.3f, %.3f)\n" % (goal_x, goal_y)

    goal(goal_x, goal_y)
    turn(theta0-theta)

def go_forward(dis):
    print "\n####################Going forward####################"
    strait(dis)

def go_back(dis):
    print "\n####################Going back####################"
    strait(-dis)

x = None
y = None
theta = None

LIN_VEL = checkLinearLimitVelocity(0.2)
ANG_VEL = checkAngularLimitVelocity(0.5)

rospy.init_node("turtlebot3_test", anonymous=True)
    
rate = rospy.Rate(10)

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

#sys.stdout.write("Provide goal.x: ")
#goal_x = input()
#sys.stdout.write("Provide goal.y: ")
#goal_y = input()

rospy.on_shutdown(shut_down)

for _ in range(4):
    go_forward(0.5)
    right_turn(90)
