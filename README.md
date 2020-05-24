# Airbnb API

Python, Django, AWS, HTML, CSS, Vanilla JS, Tailwind CSS, Gulp

## Git Description

1. git init
2. git remote add origin https://github.com/SeokRae/python_airbnb-clone.git

## Project Setting

0. db.sqlite3 삭제
1. pipenv install
2. pipenv shell
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser | python manage.py seed_superuser
6. `django_seed/__init__.py/Seed/faker`
   - 35 line: cls.fakers[code].seed(random.randint(1, 10000)) > cls.fakers[code].seed_instance(random.randint(1, 10000))
7. python manage.py seed_users --number 30
8. python manage.py seed_photos
9. python manage.py seed_amenities
10. python manage.py seed_facilities
11. python manage.py seed_houseRules
12. python manage.py seed_roomType
13. python manage.py seed_rooms --number 100
14. python manage.py seed_reservations
15. python manage.py seed_reservations --number 20

### Program Actions

- Rooms

  - [x] List Rooms
  - [x] Create Room
  - [x] Room Detail Page
  - [x] Update Room Info Page
  - [x] Room Photo Detail Page
  - [x] Add Room Photo page
  - [x] Delete Room Photo
  - [x] Update Room Photo
  - [x] Search Room

- Users

  - [x] Login
  - [x] Logout
  - [x] GitHub Login
  - [x] Kakao Login
  - [x] Create Account
  - [x] Mail verify
  - [x] User Profile Page
  - [x] Update User Profile
  - [x] Update User Password

- Reservations

  - [x] Create Reservation
  - [x] Detail Reservation Page
  - [x] Update Reservation Info Page
  - [x] Confirm Guest Room's State
  - [x] Confirm Host Room's State

- Reviews

  - [x] Create Review

- Conversations

  - [x] See Conversation
  - [x] Create Conversation

- lists
  - [x] Add Room to Favourites
  - [x] See favorite Room List
