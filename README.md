# About
**C**ommon **B**oard **G**ames **Lib**rary Dataset editor is an graphical user interface made for creating and labeling image data. 
Labeled data can be "enhanced" by synthetic data by applying different filters and create an copy of original images, therefore add more source data for training.
Lastly application can train and export models using Ultralytics Yolo models, exported modes are converted to ONNX format and can be used for computer vision. 
These models can be used by CBGLIB for android devices, which provides simplified computer vision for mobile devices.


## Installation
### Required:
- Python

#### 1. Download git repository
```
git clone https://github.com/denis-fekete/cbglib_dataset_editor
cd cbglib_dataset_editor
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
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu129
pip3 install -r requirements.txt
```

#### 4. Run editor
```
python src/main.py
```