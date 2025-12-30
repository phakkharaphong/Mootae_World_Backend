# Mootae_World_Backend

Run_python -m uvicorn main:app --reload

==============================
API Document Ref: <https://fastapi.tiangolo.com/tutorial/>

Ref: <https://medium.com/@iambkpl/setup-fastapi-and-sqlalchemy-mysql-986419dbffeb>

MailService: <https://sabuhish.github.io/fastapi-mail/example/>

source venv/Scripts/activate

alembic revision --autogenerate -m "create tables"

## Upgrade And dowgrade Table

python -m alembic upgrade head

alembic upgrade head / alembic downgrade base

alembic revision --autogenerate -m "message"

pip freeze > requirements.txt

docker build -t fastapi-app . --no-cache
