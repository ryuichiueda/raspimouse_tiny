# SPDX-FileCopyrightText: 2022 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from std_msgs.msg import UInt16
from raspimouse_tiny_msgs.action import Music

class Buzzer:
    def __init__(self):
        rclpy.init()
        self.node = Node("buzzer")
        self.pub = self.node.create_subscription(UInt16, "buzzer", self.cb, 10)
        rclpy.spin(self.node)

    def cb(self, msg):
        try:
            with open('/dev/rtbuzzer0','w') as f:
                f.write(str(msg.data) + "\n")
        except:
            self.node.get_logger().info("cannot open /dev/rtbuzzer0")


#def music_cb(goal_handle):
#    global node
#    node.get_logger().info('Executing goal...')
#    result = Music.Result()
#    return result


def main():
    node = Buzzer()
    #rclpy.init()
    #node = Node("buzzer")
    #pub = node.create_subscription(UInt16, "buzzer", cb, 10)
#    music_server = ActionServer(node, Music, 'music', music_cb)
 #   rclpy.spin(node)


if __name__ == '__main__':
    main()
