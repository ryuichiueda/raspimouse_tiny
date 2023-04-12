# SPDX-FileCopyrightText: 2022 Ryuichi Ueda 　　　　　
# SPDX-License-Identifier: BSD-3-Clause
import rclpy, time
from rclpy.node import Node
from std_msgs.msg import UInt16
from raspimouse_tiny_msgs.srv import PutMotorFreqs
from raspimouse_tiny_msgs.srv import SwitchMotors
from raspimouse_tiny_msgs.msg import MotorFreqs
from geometry_msgs.msg import Twist

def switch_motors(node, onoff):
    client = node.create_client(SwitchMotors, '/switch_motors')
    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('待機中')
 
    req = SwitchMotors.Request()
    req.on = onoff
    future = client.call_async(req)

    while rclpy.ok():
        rclpy.spin_once(node)
        if future.done():     #終わっていたら
            try:
                res = future.result() #結果を受取り
            except:
                node.get_logger().info('呼び出し失敗')
            else: #このelseは「exceptじゃなかったら」という意味のelse
                node.get_logger().info("age: {}".format(res.accepted))
            break #whileを出る

def buzzer(node):
    node.get_logger().info("test of the buzzer")
    pub = node.create_publisher(UInt16, '/buzzer', 10)
    msg = UInt16()
    msg.data = 1000
    pub.publish(msg)
    time.sleep(2.0)
    msg.data = 0
    pub.publish(msg)

def publish_motor(pub, left, right):
    d = MotorFreqs()
    d.left = left
    d.right = right
    pub.publish(d)

def motor(node):
    node.get_logger().info("test of the motors")
    pub = node.create_publisher(MotorFreqs, '/motor_raw', 10)
    publish_motor(pub,0,0)
    time.sleep(0.5)
    publish_motor(pub,-300,300)
    time.sleep(0.5)
    publish_motor(pub,0,0)
    time.sleep(0.5)
    publish_motor(pub,300,-300)
    time.sleep(0.5)
    publish_motor(pub,0,0)

def main():
    rclpy.init()
    node = Node("checker")

    buzzer(node)

    switch_motors(node, True)
    motor(node)
    switch_motors(node, False)

if __name__ == '__main__':
    main()
