#!/usr/bin/env python

import rospy
import serial
import string
import math
import sys

from sensor_msgs.msg import Imu
from tf.transformations import quaternion_from_euler

degrees2rad = math.pi/180.0

rospy.init_node("bosch_node")
#We only care about the most recent measurement, i.e. queue_size=1
pub = rospy.Publisher('imu', Imu, queue_size=1)
imuMsg = Imu()
imuMsg.orientation_covariance = [
0.0025 , 0 , 0,
0, 0.0025, 0,
0, 0, 0.0025
]

default_port='/dev/ttyACM0'
port = rospy.get_param('~port', default_port)
# Check your COM port and baud rate
rospy.loginfo("Opening %s...", port)
try:
    ser = serial.Serial(port=port, baudrate=115200, timeout=1)
except serial.serialutil.SerialException:
    rospy.logerr("IMU not found at port "+port + ". Did you specify the correct port in the launch file?")
    #exit
    sys.exit(0)
roll=0
pitch=0
yaw=0
seq=0

rospy.sleep(1) 

rospy.loginfo("Flushing first 200 IMU entries...")
for x in range(0, 200):
    line = ser.readline()
rospy.loginfo("Publishing IMU data...")
#f = open("raw_imu_data.log", 'w')

while not rospy.is_shutdown():
    line = ser.readline()
    words = string.split(line,",")    # Fields split
    if len(words) > 2:
        yaw_deg = float(words[4])
        yaw_deg = yaw_deg
        if yaw_deg > 180.0:
            yaw_deg = yaw_deg - 360.0
        if yaw_deg < -180.0:
            yaw_deg = yaw_deg + 360.0
        yaw = yaw_deg*degrees2rad
        pitch = -float(words[5])*degrees2rad
        roll = float(words[6])*degrees2rad

        imuMsg.linear_acceleration.x = 0
        imuMsg.linear_acceleration.y = 0
        imuMsg.linear_acceleration.z =0
	imuMsg.angular_velocity.x=0
	imuMsg.angular_velocity.y=0
	imuMsg.angular_velocity.z = 0

    #q = quaternion_from_euler(roll,pitch,yaw)
    imuMsg.orientation.x = float(words[1]) 
    imuMsg.orientation.y = float(words[2])
    imuMsg.orientation.z = float(words[3]) 
    imuMsg.orientation.w = float(words[0]) 
    imuMsg.header.stamp= rospy.Time.now()
    imuMsg.header.frame_id = 'base_imu_link'
    imuMsg.header.seq = seq
    seq = seq + 1
    pub.publish(imuMsg)

ser.close
#f.close
