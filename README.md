pipenv run alembic init -t async migrations
pipenv run alembic revision --autogenerate -m 'fixed column date in user model'
pipenv run alembic upgrade head


Запуск:
pipenv run uvicorn src.main:app --reload
