fmt:
	black . && isort .

test:
	pytest tests