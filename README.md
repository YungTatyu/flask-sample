## 環境構築
install sqlite3
```sh 
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
flask db upgrade
```

## lint and format
```
make lint
make fmt
```

## Test
```
make test
```
