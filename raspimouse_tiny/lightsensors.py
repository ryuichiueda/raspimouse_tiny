# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from raspimouse_tiny_msgs.msg import LightSensorValues

class LightSensors():
    def __init__(self, node_ref):
        self.node = node_ref
        self.node.declare_parameter("freq", 10)
        self.pub = self.node.create_publisher(LightSensorValues, "lightsensors", 10)
        self.freq = self.node.get_parameter("freq").value
        self.timer = self.node.create_timer(1/self.freq, self.cb)

    def cb(self):
        if self.freq != self.node.get_parameter("freq").value:
            self.freq = self.node.get_parameter("freq").value
            self.timer.destroy()
            self.timer = self.node.create_timer(1/self.freq, self.cb)

        devfile = '/dev/rtlightsensor0'
        try:
            with open(devfile, 'r') as f:
                data = f.readline().split()
                #self.node.get_logger().info("data: %s" % data[0])
                msg = LightSensorValues()
                msg.right_forward = int(data[0])
                msg.right_side = int(data[1])
                msg.left_side = int(data[2])
                msg.left_forward = int(data[3])
                self.pub.publish(msg)
        except:
            self.node.get_logger().info("cannot publish")

def main():
    rclpy.init()
    node = Node("lightsensors")
    talker = LightSensors(node)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
