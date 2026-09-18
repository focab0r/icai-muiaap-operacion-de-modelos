# Train project #

## Installation ##

First sync the libs using `uv`:
```
$> uv sync
```
Then run the project:
```
$> uv run --frozen python -m wine_quality.train
```
Run the tests on the project (just for devs)
```
$> uv run --frozen pytest
```


## Project structure ##

```
.
├── data
│   └── raw
│       └── WineQT.csv
├── pyproject.toml
├── README.md
├── src
│   └── wine_quality
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-314.pyc
│       │   └── train.cpython-314.pyc
│       └── train.py
├── tests
│   ├── __pycache__
│   │   └── test_train.cpython-314-pytest-9.1.1.pyc
│   └── test_train.py
└── uv.lock

8 directories, 10 files
```