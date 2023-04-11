# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from raspimouse_tiny_msgs.msg import Switches


class RtSwitches():
    def __init__(self, node_ref):
        self.node = node_ref
        self.pub = self.node.create_publisher(Switches, "switches", 10)
        self.node.create_timer(0.1, self.cb)

        self.d = Switches()
        self.d.state = 'neutral'
        self.state_change_counter = 0

    def cb(self):
        devfile = '/dev/rtswitch'
        try:
            with open(devfile + '0','r') as f:
                self.d.front = True if '0' in f.readline() else False
            with open(devfile + '1','r') as f:
                self.d.center = True if '0' in f.readline() else False
            with open(devfile + '2','r') as f:
                self.d.rear = True if '0' in f.readline() else False
        except:
            self.node.get_logger().info("cannot publish")

        if self.d.front: self.state_change_counter += 1
    
        if self.state_change_counter >= 5 and not self.d.front:
            self.state_change_counter = 0
            if self.d.state == 'neutral': self.d.state = 'ready' 
            elif self.d.state == 'ready': self.d.state = 'run' 
            else:                         self.d.state = 'neutral'
    
        self.pub.publish(self.d)
#        try:
#            with open(devfile, 'r') as f:
#                data = f.readline().split()
#                #self.node.get_logger().info("data: %s" % data[0])
#                msg = LightSensorValues()
#                msg.right_forward = int(data[0])
#                msg.right_side = int(data[1])
#                msg.left_side = int(data[2])
#                msg.left_forward = int(data[3])
#                self.pub.publish(msg)
#        except:
#            self.node.get_logger().info("cannot publish")


def main():
    rclpy.init()
    node = Node("switchess")
    talker = RtSwitches(node)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
