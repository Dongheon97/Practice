# Android Studio Tutorial

# Docker
  - mysql

# venv
  - python3 -m venv .venv
  - source .venv/bin/activate
  - conda deactivate

# YoloV5
  - train : python3 train.py --data /data.yaml --weights /yolov5s.yaml
  - detect : python3 detect.py --weights best.py --source /img.jpy --img 640 --batch 32 --epochs 50
# test
