## Members
- Vũ Văn An (Quality Assurance)

## Overview
```
app
├─ README.md
├─ app.py
├─ logs
├─ note.md
├─ requirements.txt
├─ src
│  ├─ README.md
│  ├─ scripts
│  ├─ style
│  ├─ test
│  ├─ tools
│  └─ utils
└─ user_data
```

## Getting started

- Create and activate venv
- Install dependencies
```python
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
pip install uv
```
- Run app
```
uv run -m app
```