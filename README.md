# backend
Backend


Env build 
```sh
conda env create -n myenv2 -f environment.yml
```
make sure to add

```sh
pip install fastapi[standard]
```
and
```sh
playwright install chromium
```

conda one does not work currently

Env export
```sh
conda env export --no-builds > environment.yml
```



## DB init
run `python init_db.py`



## Running
After you installed and set up database run `fastapi dev main.py` from `root`
