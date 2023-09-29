import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

from PIL import Image as Img

import torch
from torch import unsqueeze
from torchvision.io.image import read_image, ImageReadMode
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
from torchvision.transforms import ToPILImage
from torchvision import transforms

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np


class HumanDetectionFasterRCNN(Node):
    def __init__(self):
        super().__init__('human_detection_fasterrcnn')
        self.bridge = CvBridge()
        self.human_sub = self.create_subscription(
            Image, "camera", self.human_detection_callback, 10)
        self.faster_pub = self.create_publisher(
            Image, "faster_rcnn_inference", 1)
        self.get_logger().info("Faster RCNN node is inititalized...")

    def human_detection_callback(self, msg):
        try:
            img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(e)

        # Step 1: Initialize model with the best available weights
        weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        model = fasterrcnn_resnet50_fpn_v2(
            weights=weights, box_score_thresh=0.9)
        model.eval()

        # Step 2: Initialize the inference transforms
        img = Img.fromarray(img)
        tensor_transform = transforms.Compose([transforms.PILToTensor()])
        tensor_img = tensor_transform(img)
        preprocess = weights.transforms()

        # Step 3: Apply inference preprocessing transforms
        batch = preprocess(tensor_img)
        batch = batch.unsqueeze(0)

        # Step 4: Use the model and visualize the prediction
        prediction = model(batch)[0]
        
        labels = [weights.meta["categories"][i]
                  for i in prediction["labels"]]

        box = draw_bounding_boxes(tensor_img, boxes=prediction["boxes"],
                                  labels=labels,
                                  colors="red",
                                  width=4)
        
        im = to_pil_image(box.detach())     # <class 'PIL.Image.Image'>
        img = np.array(im)
        self.get_logger().info(f"{type(img)}")                  # pil to numpy array
        img_msg = self.bridge.cv2_to_imgmsg(img)

        self.faster_pub.publish(img_msg)


def main(args=None):
    rclpy.init(args=args)
    node = HumanDetectionFasterRCNN()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
