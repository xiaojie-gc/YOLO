from streamparse import Bolt
import os


class CompareBolt(Bolt):
    outputs = ["compare"]

    def initialize(self, conf, ctx):
        self.pid = os.getpid()
        self.resutls = []


    """
    tup  = (name, [cpu, time], index, detections)
    """
    def process(self, tup):
        exists = False
        idx = -1
        for i in range(len(self.resutls)):
            item = self.resutls[i]
            if item["idx"] == tup.values[2]:
                exists = True
                idx = i
                break
        if not exists:
            self.resutls.append({"idx": tup.values[2], "YOLO416": None, "YOLO256": None, "YOLO608": None})

        self.resutls[idx][tup.values[0]] = {
            "cpu": tup.values[1][0],
            "process_latency": tup.values[1][1]
        }

        if self.resutls[idx]["YOLO416"] is not None and self.resutls[idx]["YOLO256"] is not None and self.resutls[idx]["YOLO608"] is not None:
            analysis = {
                "index": self.resutls[idx]["idx"],
                "YOLO_416_EX_TIME": self.resutls[idx]["YOLO416"]["process_latency"],
                "YOLO_256_EX_TIME": self.resutls[idx]["YOLO256"]["process_latency"],
                "YOLO_608_EX_TIME": self.resutls[idx]["YOLO608"]["process_latency"],

                "YOLO_416_CPU": self.resutls[idx]["YOLO416"]["cpu"],
                "YOLO_256_CPU": self.resutls[idx]["YOLO256"]["cpu"],
                "YOLO_608_CPU": self.resutls[idx]["YOLO608"]["cpu"],

            }
            self.emit([analysis])
            self.resutls.pop(idx)