# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from raspimouse_tiny_msgs.msg import LightSensorValues

class Talker():
    def __init__(self, node_ref):
        self.node = node_ref
        self.pub = self.node.create_publisher(LightSensorValues, "rtlightsensors", 10)
        self.node.create_timer(0.1, self.cb)

    def cb(self):
        devfile = '/dev/rtlightsensor0'
        d = LightSensorValues()
        try:
            with open(devfile,'r') as f:
                data = f.readline().split()
                d = LightSensorValues()
                d.right_forward = int(data[0])
                d.right_side = int(data[1])
                d.left_side = int(data[2])
                d.left_forward = int(data[3])
                self.pub.publish(d)
        except:
            self.node.logerr("cannot open " + devfile)

def main():
    rclpy.init()
    node = Node("rtlightsensors")
    talker = Talker(node)
    rclpy.spin(node)
