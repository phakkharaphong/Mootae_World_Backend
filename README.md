# Mootae_World_Backend
Run_python -m uvicorn main:app --reload

==============================
API Document Ref: https://fastapi.tiangolo.com/tutorial/

Ref: https://medium.com/@iambkpl/setup-fastapi-and-sqlalchemy-mysql-986419dbffeb


source venv/Scripts/activate

alembic revision --autogenerate -m "create tables"
## Upgrade And dowgrade Table 
alembic upgrade head / alembic downgrade base 

