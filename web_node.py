#!/usr/bin/env python
import rospy
import subprocess
import time
import os
from std_msgs.msg import Int16


def callback(data):
    if (data.data==1):
	package = subprocess.Popen('./launch.sh &',shell=True)
    if (data.data==2):
	another = subprocess.Popen('./roscore.sh &',shell=True)
    if (data.data==3):
	kill = subprocess.Popen('./killXterm.sh &',shell=True)

  
def webNode():
    rospy.init_node('web_node', anonymous=True)
    rospy.Subscriber("website", Int16, callback)


    rospy.spin()

if __name__ == '__main__':
    webNode()
