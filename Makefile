.PHONY: run

# Run the server
run:
	bash -c "source venv/bin/activate && python -m uvicorn app.main:app --reload"