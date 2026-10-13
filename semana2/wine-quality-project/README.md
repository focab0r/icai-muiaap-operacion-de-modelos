# Wine prediction #

This project is the origin of the future work we will be doing in wine prediction.

The project must be runned from the root of the repo. If not, just omit the `--project` argument.

## Usage ##

1. Download and prepare the environment using `uv`:
```
$> uv sync --project semana2/wine-quality-project/ --locked

Resolved 19 packages in 1ms
Checked 17 packages in 0.48ms
```

2. Run the project:
```
$> uv run --project semana2/wine-quality-project/ --frozen python -m wine_quality.train

Training model...
Filas: 1143
Variables: 11
Clases: 6
F1 macro: 0.3402
```

## For devs ##

1. Run the tests on the project 
```
$> uv run --project semana2/wine-quality-project/ --frozen pytest semana2/wine-quality-project/

================================= test session starts =================================
platform linux -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: [REDACTED]/icai-muiaap-operacion-de-modelos/semana2/wine-quality-project
configfile: pyproject.toml
collected 1 item

tests/test_train.py .                                                          [100%]

================================= 1 passed in 1.58s =================================
                                                                                                       
```

2. Use `ruff` to check the syntax format
```
$> uv run --project semana2/wine-quality-project/ --frozen ruff check ./semana2/wine-quality-project/

All checks passed!
```


## Project structure ##

```
.
├── data
│   └── raw
│       └── WineQT.csv      # Data for the model
├── pyproject.toml          # Dependencies of the project. Managed by uv
├── README.md
├── src
│   └── wine_quality
│       ├── __init__.py     # Create the package
│       └── train.py        # Train the model
├── tests
│   └── test_train.py       # Include 1 test
└── uv.lock                 # Used to run the same code as the author

8 directories, 10 files
```