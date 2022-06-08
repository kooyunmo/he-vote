# he-vote

Voting system based on additive symmetric homomorphic encryption

## Preparation

```sh
# Install deps
$ pip install -r requirements.txt

$ cd hevote

# Migration
$ python manage.py migrate

# Craete super-user
$ python manage.py createsuperuser

# Run server
$ python manage.py runserver
```

1. Go to `http://localhost:8000/admin` and login with your superuser account.
2. Go to `Candidate` table and add "Washington", "Adams", and "Jefferson" exactly in the order.

## Swagger

Go to `http://localhost:8000/api/schema/swagger-ui/#` and test REST APIs.
