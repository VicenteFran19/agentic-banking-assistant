.PHONY: install test eval eval-offline chat api docker
install:
	pip install -r requirements.txt
test:
	python -m pytest -q
eval:
	python eval/run_eval.py --check
eval-offline:
	python eval/run_eval.py --provider fake --check
chat:
	cd src && python -m assistant.cli
api:
	uvicorn assistant.api:app --app-dir src --reload
docker:
	docker build -t agentic-banking-assistant . && docker run --rm -p 8000:8000 --env-file .env agentic-banking-assistant
