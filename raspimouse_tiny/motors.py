# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from raspimouse_tiny_msgs.msg import LightSensorValues

class Motors():
    def __init__(self, node_ref):
        self.node = node_ref
        #self.pub = self.node.create_publisher(LightSensorValues, "motors", 10)
        #self.node.create_timer(0.1, self.cb)

        self.sub_freqs = rospy.Subscriber('motor_raw', MotorFreqs, callback_motor_raw)
        self.sub_cmd_vel = rospy.Subscriber('cmd_vel', Twist, callback_cmd_vel)
        self.srv_motor_power = rospy.Service('switch_motors', SwitchMotors, callback_motor_sw)
        self.srv_freqs = rospy.Service('put_motor_freqs', PutMotorFreqs, callback_put_freqs)

    def cb(self):
        pass
#        devfile = '/dev/rtlightsensor0'
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
    node = Node("motors")
    talker = Motors(node)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
