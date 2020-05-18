# A simple Directed acyclic graph (DAG) and Apache storm setting

1. Cameras/Image folders Codes: src/spouts 
- Spouts: read source images and get image's byte-string (use base64.encodebytes)
2. Computation Tasks Codes: src/bolts
- detection_img -Bolts: receive byte-string from specific spouts and convert it back image object (use base64.b64decode)

3. Topology: topologies/yolo.py



