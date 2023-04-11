# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy
from rclpy.node import Node
from raspimouse_tiny_msgs.srv import PutMotorFreqs
from raspimouse_tiny_msgs.srv import SwitchMotors

class Motors():
    def __init__(self, node_ref):
        self.node = node_ref
        #self.pub = self.node.create_publisher(LightSensorValues, "motors", 10)
        #self.node.create_timer(0.1, self.cb)

        #self.sub_freqs = rospy.Subscriber('motor_raw', MotorFreqs, self.callback_motor_raw)
        #self.sub_cmd_vel = rospy.Subscriber('cmd_vel', Twist, self.callback_cmd_vel)
        self.srv_motor_power = self.node.create_service(SwitchMotors, 'switch_motors', self.callback_motor_sw)
        self.srv_freqs = self.node.create_service(PutMotorFreqs, 'put_motor_freqs', self.callback_put_freqs)

    def callback_motor_sw(self, request, response):
        enfile = '/dev/rtmotoren0'
        try:
            with open(enfile,'w') as f:
                if request.on: f.write("1\n")
                else:          f.write("0\n")
            response.accepted = True
        except:
            self.node.get_logger().info("cannot write to " + enfile)
            response.accepted = False

        return response    

    def callback_put_freqs(self, request, response):
        devfile = '/dev/rtmotor0'
        try:
            with open(devfile,'w') as f:
                f.write("%s %s %s\n" % (request.left, request.right, request.duration))
            response.accepted = True
        except:
            rospy.logerr("cannot write to " + devfile)
            response.accepted = False

        return response    


def main():
    rclpy.init()
    node = Node("motors")
    talker = Motors(node)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
