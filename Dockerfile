FROM --platform=$TARGETPLATFORM python:3.12-slim

WORKDIR /app
COPY . /app

CMD ["python", "-m", "src.memory_agent_benchmark", "--dataset", "examples/learning_notes.jsonl"]

