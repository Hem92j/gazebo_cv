#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

import torch
from torch import unsqueeze
from torchvision.io.image import read_image, ImageReadMode
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image
from torchvision.transforms import transforms, ToTensor
from PIL import Image as Img

from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

from faster_rcnn.msg import InferenceResult
from faster_rcnn.msg import FasterRcnn

bridge = CvBridge()


class Camera_subscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        self.bridge = CvBridge()
        self.weights = FasterRCNN_ResNet50_FPN_V2_Weights.DEFAULT
        self.model = fasterrcnn_resnet50_fpn_v2(
            weights=self.weights, box_score_thresh=0.9)

        self.faster_rcnn_inference = FasterRcnn()

        self.subscription = self.create_subscription(
            Image,
            'camera',
            self.camera_callback,
            10)

        self.yolov8_pub = self.create_publisher(
            FasterRcnn, "faster_rcnn_inf_publisher", 1)
        self.img_pub = self.create_publisher(Image, "/inference_result", 1)
        self.get_logger().info("camera_publisher node is initialized...")


    def camera_callback(self, data):
        try:
            img = self.bridge.imgmsg_to_cv2(data, "bgr8")

        except CvBridgeError as e:
            self.get_logger().error(e)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Img.fromarray(img)
        
        # img = bridge.imgmsg_to_cv2(data, "bgr8")
        self.model.eval()
       
        preprocess = self.weights.transforms()
        batch = [preprocess(img)]
        
        prediction = self.model(batch)
        labels = [self.weights.meta["categories"]
                  for i in prediction["labels"]]

        self.faster_rcnn_inference.header.frame_id = "inference"
        self.faster_rcnn_inference.header.stamp = Camera_subscriber.get_clock().now().to_msg()

        for _ in prediction:
            boxes = prediction["boxes"].to("cpu").detach().numpy()
            for _ in boxes:
                self.inference_result = InferenceResult()

                self.inference_result.class_name = labels
                self.inference_result.top = int(boxes[0][0])
                self.inference_result.left = int(boxes[0][1])
                self.inference_result.bottom = int(boxes[0][2])
                self.inference_result.right = int(boxes[0][3])
                self.faster_rcnn_inference.faster_rcnn_inference.append(
                    self.inference_result)

            # camera_subscriber.get_logger().info(f"{self.yolov8_inference}")

        annotated_frame = draw_bounding_boxes(
            img, boxes=prediction["boxes"], labels=labels, colors="red", width=3)
        img_msg = bridge.cv2_to_imgmsg(annotated_frame)

        self.img_pub.publish(img_msg)
        self.yolov8_pub.publish(self.yolov8_inference)
        self.yolov8_inference.yolov8_inference.clear()


def main(args=None):
    rclpy.init(args=args)
    node = Camera_subscriber()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
