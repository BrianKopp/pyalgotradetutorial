# PyAlgoTrade Tutorial

Small library showing walkthrough of pyalgotrade tutorial

Set up environment with

```
virtualenv venv --python=python3
source venv/bin/activate
pip install pyalgotrade
```

## Step 1: Getting Sample Data

Command:

```
python -m "pyalgotrade.tools.quandl" --source-code="WIKI" --table-code="ORCL" --from-year=2000 --to-year=2000 --storage=. --force-download --frequency=daily
```
