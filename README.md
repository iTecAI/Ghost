# Ghost
Self-hosted modular download system

## Developing
Clone the repository, then `cd Ghost`

### Backend
```sh
cd server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python -m uvicorn main:app --reload --log-level debug

# And to deactivate:
deactivate
```

### Frontend
```sh
cd ghost
yarn install
yarn start
```