# SPDX-FileCopyrightText: 2022 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, time
from rclpy.node import Node
from std_msgs.msg import UInt16

def buzzer(hz, node):
    node.get_logger().info("test of the buzzer")
    pub = node.create_publisher(UInt16, '/buzzer', 10)
    msg = UInt16()
    msg.data = hz
    pub.publish(msg)

def main():
    ### buzzer test ###
    rclpy.init()
    node = Node("checker")
    buzzer(1000, node)
    time.sleep(2.0)
    buzzer(0, node)

if __name__ == '__main__':
    main()
