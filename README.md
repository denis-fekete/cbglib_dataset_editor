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