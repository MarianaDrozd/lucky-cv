# Lucky CV Maker

### CRUD with postgresql database

- POST `/APIv1/auth/user-register` - user register
- GET `/APIv1/auth/confirm-email/{token}` - confirm email
- POST `/APIv1/auth/login` - user login
- GET `/APIv1/auth/logout` - user logout

####

- GET `/APIv1/resumes` - get resumes
- GET `/APIv1/resumes/{id}` - get resume by id
- POST `/APIv1/resumes` - create resume
- PATCH `/APIv1/resumes/{id}` - update resume by id
- DELETE `/APIv1/resumes/{id}` - delete resume by id

####

- GET `/APIv1/templates` - get templates
- GET `/APIv1/templates/{id}` - get templates by id
- POST `/APIv1/templates` - create template
- PATCH `/APIv1/templates/{id}` - update template by id
- DELETE `/APIv1/templates/{id}` - delete template by id

### How to run it

 1. `pip install -r requirements.txt`
 2. `python run.py`

### By docker-compose:

 1. `docker-compose build`
 2. `docker-compose up`


