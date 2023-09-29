import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np



class ImageSubscriber(Node):
    def __init__(self):
        super().__init__("image_subscriber")

        self.declare_parameter('image_topic', "camera")
        self.topic = self.get_parameter(
            "image_topic").get_parameter_value().string_value

        self.bridge = CvBridge()

        self.sub_ = self.create_subscription(
            Image, self.topic, self.img_callback, 10)

        self.get_logger().info(
            f"Image subscriber is subscribed to {self.topic} topic")

    def img_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(e)

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        cv_image = cv2.resize(cv_image, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(cv_image, winStride=(8, 8))

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(cv_image, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
            cv2.circle(cv_image, (25, 35), 1, -1)

        # Display the resulting frame
        cv2.imshow('frame', cv_image)
        cv2.waitKey(1)


        # (row, cols, channel) = cv_image.shape
        # self.get_logger().info(f"height of the image: {row}, "
        #                        f"width of the image : {cols}, "
        #                        f"color channel of the image: {channel}.", once=True)

        # cv2.circle(cv_image, (50, 50), 10, 255, thickness=-1)

        # cv2.imshow("image_window", cv_image)
        # cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
