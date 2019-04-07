#!/bin/sh

MASTER=$(echo $ROS_MASTER_URI | cut -c 8- | cut -d':' -f 1)

while [ true ]; do
  sleep 1
  ping -c1 $MASTER > /dev/null 2>&1

  if [ $? != 0 ]
  then
    rosrun turtlebot3_automation turtlebot3_autonomous.py
    break
  fi
done
