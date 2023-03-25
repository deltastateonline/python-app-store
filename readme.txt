export FLASK_ENV=development

docker build -t rest-api-flask-python
docker run -p 5005:5000 rest-api-flask-python
