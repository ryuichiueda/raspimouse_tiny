# SPDX-FileCopyrightText: 2022 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, time
from rclpy.node import Node
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from std_msgs.msg import UInt16
from raspimouse_tiny_msgs.action import Music

class Buzzer:
    def __init__(self):
        rclpy.init()
        self.node = Node("buzzer")
        self.pub = self.node.create_subscription(UInt16, "buzzer", self.cb, 10)
        self.music_server = ActionServer(self.node, Music, 'music', self.music_cb, cancel_callback=self.music_cancel)
        rclpy.spin(self.node)

    def buz(self, freq):
        try:
            with open('/dev/rtbuzzer0','w') as f:
                f.write(str(freq) + "\n")
        except:
            self.node.get_logger().info("cannot open /dev/rtbuzzer0")


    def cb(self, msg):
        self.buz(msg.data)


    def music_cancel(self, goal):
        self.node.get_logger().info("!!!!")
        return CancelResponse.ACCEPT


    def music_cb(self, goal_handle):
        self.node.get_logger().info('Executing goal: {}'.format(goal_handle.request))

        result = Music.Result()
        feedback = Music.Feedback()
        result.finished = False
        for i, f in enumerate(goal_handle.request.freqs):
            if not goal_handle.is_active:
                return result

            feedback.remaining_steps = len(goal_handle.request.freqs) - i
            goal_handle.publish_feedback(feedback)
            self.buz(f)
            time.sleep(goal_handle.request.durations[i])

        goal_handle.succeed()
        result.finished = True
        return result


def main():
    node = Buzzer()


if __name__ == '__main__':
    main()
