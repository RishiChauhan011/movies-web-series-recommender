# Using Windows commands (install make via chocolatey or use generic run commands)

SERVER_CMD = python -m backend.app.main
FRONTEND_CMD = streamlit run frontend/app.py

.PHONY: run-server run-frontend install

install:
	pip install -r requirements.txt

run-server:
	$(SERVER_CMD)

run-frontend:
	$(FRONTEND_CMD)
