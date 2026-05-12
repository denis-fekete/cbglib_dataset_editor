# About
**Dataset Creator** is part of the **Computer Vision Library for Board Games** or **CVLiBG** workflow. 
It is a desktop application for annotating image data, creating additional synthetic data, and train 
custom fine-tuned models for object detection tasks.

Pre-trained models are provided by the Ultralytics, and this application utilizes its YOLO models for 
training custom object detection models.

Models are exported into ONNX format. These models, can be further used for automatic annotation. 


## Installation
### Required:
- Python 3.10
- Pip

#### 1. Download git repository
```
git clone https://github.com/denis-fekete/cvlibg-dataset-creator.git
cd cvlibg-dataset-creator
```

#### 2. Create python virtual environment (not mandatory but recommended)
```
py -3.10 -m venv venv
```

#### 3. Activate environment
Linux:
`source venv/bin/activate`
Windows:
`.\venv\Scripts\activate`

#### 3. Install dependencies
```
pip3 install .
```
or for development
```
pip3 install -e .
```
#### 4. Install torch torchvision
```
pip install torch torchvision 
```
Or, to use **GPU** for training, install a compatible version of torch and torchvison, for more details see (https://pytorch.org/get-started/locally/)[https://pytorch.org/get-started/locally/].
```
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu129
```

#### 5. Open Dataset Creator
```
dataset-creator
```