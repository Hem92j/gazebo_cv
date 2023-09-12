import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError
import cv2 


class ImagePublihser(Node):
    def __init__(self):
        super().__init__("image_publisher")

        self.declare_parameter('image_topic', "cam_publisher")
        self.topic = self.get_parameter("image_topic").get_parameter_value().string_value

        self.pub = self.create_publisher(Image, self.topic, 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)
        self.get_logger().info(f"Image Publisher is publishing on {self.topic} topic")

    def timer_callback(self):
        ret, frame = self.cap.read()
        try:
            self.pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            self.get_logger().error(e)


def main(args = None):
    rclpy.init(args = args)
    node =ImagePublihser()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()