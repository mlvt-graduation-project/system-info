# create_revision:
# 	alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

# %:
# 	@:

# upgrade_head:
# 	alembic upgrade head

# downgrade:
# 	alembic downgrade

postgres:
	python3.11 Postgres/Postgres_connect.py

postgres_up:
	python3.11 Postgres/migrate_up.py

postgres_down:
	python3.11 Postgres/migrate_down.py

mongo:
	python3.11 MongoDB/MongoDB_connect.py

install_requirement:
	python3.11 -m pip install -r requirements.txt 