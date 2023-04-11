# SPDX-FileCopyrightText: 2023 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, math
from rclpy.node import Node
from raspimouse_tiny_msgs.srv import PutMotorFreqs
from raspimouse_tiny_msgs.srv import SwitchMotors
from raspimouse_tiny_msgs.msg import MotorFreqs
from geometry_msgs.msg import Twist

class Motors():
    def __init__(self, node_ref):
        self.node = node_ref
        #self.pub = self.node.create_publisher(LightSensorValues, "motors", 10)
        #self.node.create_timer(0.1, self.cb)

        self.sub_freqs = self.node.create_subscription(MotorFreqs, 'motor_raw', self.callback_motor_raw, 10)
        self.sub_cmd_vel = self.node.create_subscription(Twist, 'cmd_vel', self.callback_cmd_vel, 10)
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
            self.node.get_logger().info("cannot write to " + devfile)
            response.accepted = False

        return response    


    def callback_motor_raw(self, msg):
        lfile = '/dev/rtmotor_raw_l0'
        rfile = '/dev/rtmotor_raw_r0'
        
        try:
            lf = open(lfile,'w')
            rf = open(rfile,'w')
            lf.write("%s\n" % msg.left)
            rf.write("%s\n" % msg.right)
        except:
            self.node.get_logger().info("cannot write to rtmotor_raw_*")
    
        lf.close()
        rf.close()

    def callback_cmd_vel(self, msg):
        lfile = '/dev/rtmotor_raw_l0'
        rfile = '/dev/rtmotor_raw_r0'

        #for forwarding
        forward_hz = 80000.0*msg.linear.x/(9*math.pi)
        #for rotation
        rot_hz = 400.0*msg.angular.z/math.pi
        try:
            lf = open(lfile,'w')
            rf = open(rfile,'w')
            lf.write(str(int(round(forward_hz - rot_hz))) + '\n')
            rf.write(str(int(round(forward_hz + rot_hz))) + '\n')
        except:
            self.node.get_logger().info("cannot write to rtmotor_raw_*")
    
        lf.close()
        rf.close()


def main():
    rclpy.init()
    node = Node("motors")
    talker = Motors(node)
    rclpy.spin(node)


if __name__ == '__main__':
    main()
