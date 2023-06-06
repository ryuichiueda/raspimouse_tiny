#!/bin/bash

ros2 action send_goal --feedback music raspimouse_tiny_msgs/action/Music '{freqs: [ 349,392,440,466,523,587,622,698,784,0 ], durations: [0.6,0.3,0.3,0.2,0.2,0.2,0.2,0.2,3.0,1.0]}' & 

sleep 1

ros2 service call /action/music/_action/cancel_goal action_msgs/CancelGoal '{}'
