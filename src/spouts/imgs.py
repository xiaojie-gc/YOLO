from itertools import cycle

from streamparse import Spout
from database.connector import SQLConnector
import time
import base64


class ImgSpout(Spout):
    outputs = ["img_name", "img_data"]

    def initialize(self, stormconf, context):
        self.names = cycle(["dog.jpg", "eagle.jpg", "person.jpg", "room.jpg", "giraffe.jpg", "field.jpg"])
        self.images_path = "/home/ubuntu/data/samples"
        self.next_id = 1

    def next_tuple(self):
        connector = SQLConnector()
        next_id = connector.get_last_index()
        if next_id == self.next_id - 1:
            name = next(self.names)
            with open(self.images_path + "/" + name, 'rb') as file:
                data = file.read()
            img_data = base64.encodebytes(data).decode("utf-8")
            self.emit([name, img_data], tup_id=self.next_id)
            self.next_id += 1
        else:
            time.sleep(0.1)
            self.logger.info("waiting the last ID={}".format(next_id))
        connector.disconnect()