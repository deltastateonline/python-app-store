```
export FLASK_ENV=development

pip install -r requirements.txt
docker build -t rest-api-flask-python .
docker run -dp 5005:5000  -w /app -v "$(pwd):/app" rest-api-flask-python sh -c "flask run --host 0.0.0.0"

docker ps
docker container stop

flask db init
flask db migrate
flask db upgrade

```

