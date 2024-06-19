## Pi - Challenge Python
___
### Requirements:
 - docker
 - docker-compose
 - python 3.11
 - git
 - virtualenv
 - pycharm | vscode
---

### Execute:
```bash
# clone project:
git clone git@github.com:motrandavidsanchez/pi-challenge.git

# Duplicate the .env.template file and rename it to .env
cp .env.template .env
```

---

### Run with docker-compose:
```bash
docker-compose build

docker-compose up
```

---
### Run without docker-compose
```bash
# Create virtual environment
python3 -m venv ~/.virtualenvs/pi-challenge

# Install requirements:
poetry install

# Run project
uvicorn src.main:app --reload --port 8001
```
---
### Migrations
``` bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```
---
### Test
``` bash
pytest -s -v
```