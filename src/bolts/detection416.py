import os
from collections import Counter
from itertools import cycle
from streamparse import Bolt
import torch
from torch.utils.data import DataLoader
from torch.autograd import Variable

from model.models import *
from utils.utils import *
from utils.datasets import *

import base64
import cv2

import os
import psutil
import sys
import time
import datetime
import argparse


class DetectionBolt_416(Bolt):
    outputs = ["name", "cpu", "index", "detection_results"]

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.total = 0
        self.start_time = time.time()
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if torch.cuda.is_available():
            self.tag = "GPU"
        else:
            self.tag = "CPU"

        self.logger.info("start to create YOLO....")
        # self.logger.info(conf)
        # Set up model
        try:
            self.img_size = 416
            self.model = Darknet("/home/ubuntu/config/yolov3.cfg", self.img_size).to(device)
            # Load darknet weights
            self.model.load_darknet_weights("/home/ubuntu/weights/yolov3.weights")
            self.model.eval()  # Set in evaluation mode
            self.classes = load_classes("/home/ubuntu/data/coco.names")  # Extracts class labels from file
            self.Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
        except Exception as e:
            self.logger.info(
                "fail to create YOLO model = {}".format(e)
            )
        self.logger.info("success to create YOLO on = {}".format(self.tag))


    def _increment(self):
        self.total += 1

    def process(self, tup):
        img_name, img_data = tup.values[0], tup.values[1]
        self._increment()
        img_path = "/home/ubuntu/data/inputs"
        with open(img_path + "/" + str(self.total) + "_416_" + img_name, 'wb') as file:
            file.write(base64.b64decode(img_data))
        objs, cpu, computation_time = self.detect_image(str(self.total) + "_416_" + img_name,  img_path)
        self.emit(["YOLO416", [cpu, computation_time], self.total, objs])

    def detect_image(self, img_name, images_path, conf_thres=0.8, nms_thres=0.4):
        py = psutil.Process(self.pid)
        cpu = round(py.cpu_times()[0] / (time.time() - self.start_time), 4)
        start_time = time.time()
        # Start inference
        image = cv2.imread(os.path.join(images_path, img_name), cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (self.img_size, self.img_size),
                           interpolation=cv2.INTER_LINEAR)
        image = image.astype(np.float32)
        image /= 255.0
        image = np.transpose(image, (2, 0, 1))
        image = image.astype(np.float32)
        input_imgs = []
        input_imgs.append(image)
        input_imgs = np.asarray(input_imgs)
        input_imgs = torch.from_numpy(input_imgs)
        # Configure input
        input_imgs = Variable(input_imgs.type(self.Tensor))
        # Get detections
        img_detections = []
        with torch.no_grad():
            detections = self.model(input_imgs)
            detections = non_max_suppression(detections, conf_thres, nms_thres)
        img_detections.extend(detections)
        objs = []
        for detection in detections:
          if detection is not None:
            for x1, y1, x2, y2, conf, cls_conf, cls_pred in detection:
                objs.append(self.classes[int(cls_pred)])
        computation_time = round(time.time() - start_time, 4)
        self.logger.info("pid = {}, cpu = {}, execution time={}, objs={}".format(self.pid, cpu, computation_time, objs))
        return objs, cpu, computation_time


