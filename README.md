# About
Computer Vision Library for Board Games or CVLiBG's Dataset Creator is an graphical user interface made for creating and labeling image data. 
Labeled data can be "enhanced" by synthetic data by applying different filters and create an copy of original images, therefore add more source data for training.
Lastly application can train and export models using Ultralytics Yolo models, exported modes are converted to ONNX format and can be used for computer vision. 
These models can be used by CBGLIB for android devices, which provides simplified computer vision for mobile devices.


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