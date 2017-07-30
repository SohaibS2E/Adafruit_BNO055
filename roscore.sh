#!/bin/bash
source /opt/ros/indigo/setup.bash
source ~/wall2e/devel/setup.bash
xterm -e "rosrun imu_complementary_filter complementary_filter_node"
