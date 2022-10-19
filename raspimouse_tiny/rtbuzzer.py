# SPDX-FileCopyrightText: 2022 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16


def cb(msg):
    global node
    try:
        with open('/dev/rtbuzzer0','w') as f:
            f.write(str(msg.data) + "\n")
    except:
        node.get_logger().info("cannot open /dev/rtbuzzer0")


def main():
    rclpy.init()
    node = Node("rtbuzzer")
    pub = node.create_subscription(UInt16, "rtbuzzer", cb, 10)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
