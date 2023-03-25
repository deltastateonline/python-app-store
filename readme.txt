export FLASK_ENV=development

docker build -t rest-api-flask-python .
docker run -dp 5005:5000  -w /app -v "$(pwd):/app" rest-api-flask-python
