#!/bin/bash

# This script opens terminals for the following:
# 1 - ssh nvidia@10.42.0.218
# 1.1 - ssh nvidia@10.42.0.218
# 2 - roscore
# 2.1 - roslaunch youbot_bringup final.launch
# 2.2 - roslaunch aricc_2d_vision kennydlv2.launch
# 2.3 - roslaunch aricc_test bringup.launch
# 3 - roslaunch youbot_bringup gripper.launch
# 4 - rosservice call /move_base_node/clear_costmap

gnome-terminal --tab -e "bash -c 'ssh nvidia@10.42.0.218';bash" --tab -e "bash -c 'ssh nvidia@10.42.0.218';bash"
gnome-terminal --tab -e "bash -c 'roscore';bash" --tab -e "bash -c 'roslaunch youbot_bringup final.launch';bash" --tab -e "bash -c 'roslaunch aricc_2d_vision kennydlv2.launch';bash" --tab -e "bash -c 'roslaunch aricc_test bringup.launch';bash" --tab -e "bash -c 'roslaunch youbot_bringup gripper.launch';bash"
gnome-terminal -e "bash -c 'roslaunch youbot_bringup gripper.launch';bash"
gnome-terminal -e "bash -c 'rosservice call /move_base_node/clear_costmap'; bash"
