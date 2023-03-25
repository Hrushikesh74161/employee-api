# Employee API

## Setting Up:

- Clone this repo.
- Create virtual environment:
> python3.11 -m venv venv
- Activate virtual environment (linux):
> source venv/bin/activate
- Install dependencies:
> pip install -r requirements.txt
- No need to migrate, prefilled sqilte db available in the repo.
- If you delete the db, then run:
> python manage.py migrate
- Mock employee data available in sql file named employees.sql, run it to insert all the data into employees table.
- Run tests:
> python manage.py test
- To run on your computer:
> python manage.py runserver
- To run in docker, Dockerfile and docker-compose file are provided.
> docker compose up

### Postman collection file is available in project root folder.

## API
Find endpoints at: http://127.0.0.1:8000/api/schema/docs

- All endpoints require basic authentication credentials, except for login, and register.

- For sending credentials set, Authorization header in request: Authorization: 'Basic username:password', username:password should be base64 encoded and should be converted to ascii from bytes.

Download Schema at:
> http://127.0.0.1:8000/api/schema