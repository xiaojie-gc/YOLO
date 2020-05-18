from streamparse import Bolt
import os
import time
from database.connector import SQLConnector


class OutputBolt(Bolt):
    outputs = ["output"]

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.resutls = []
        self.preTimer = time.time()

    def process(self, tup):
        connector = SQLConnector()
        analysis = tup.values[0]
        time_elapsed = time.time() - self.preTimer
        self.preTimer = time.time()
        # self.logger.info("total latency = {}, result = '{}'".format(time_elapsed, tup.values[0]))
        connector.insert(analysis["index"], analysis["YOLO_416_EX_TIME"], analysis["YOLO_256_EX_TIME"], analysis["YOLO_608_EX_TIME"],
                              analysis["YOLO_416_CPU"]*100, analysis["YOLO_256_CPU"]*100, analysis["YOLO_608_CPU"]*100, time_elapsed)
        connector.disconnect()
        self.emit(["done"])