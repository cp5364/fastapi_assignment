#!/bin/bash
# cd /code
# alembic stamp head
# alembic revision --autogenerate
# alembic upgrade head
uvicorn src.unisys.main:app --reload --host 0.0.0.0 --port 80

