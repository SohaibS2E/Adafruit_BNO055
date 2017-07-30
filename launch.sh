#!/bin/bash
source /opt/ros/indigo/setup.bash
source ~/wall2e/devel/setup.bash
xterm -e "roslaunch bosch_imu_pkg bosch_imu.launch"
