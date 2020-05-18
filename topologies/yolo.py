"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.detection416 import DetectionBolt_416
from bolts.detection256 import DetectionBolt_256
from bolts.detection608 import DetectionBolt_608
from bolts.compare import CompareBolt
from bolts.output import OutputBolt
from spouts.imgs import ImgSpout


class YOLO(Topology):

    camera_1 = ImgSpout.spec()
    camera_2 = ImgSpout.spec()
    camera_3 = ImgSpout.spec()

    task1 = DetectionBolt_416.spec(inputs={camera_1: Grouping.fields(["img_name", "img_data"])}, par=1)
    task2 = DetectionBolt_256.spec(inputs={camera_2: Grouping.fields(["img_name", "img_data"])}, par=1)
    task3 = DetectionBolt_608.spec(inputs={camera_3: Grouping.fields(["img_name", "img_data"])}, par=1)

    compare_bolt = CompareBolt.spec(inputs=[task1, task2, task3], par=1)

    OutputBolt = OutputBolt.spec(inputs={compare_bolt: Grouping.fields(["compare"])}, par=1)