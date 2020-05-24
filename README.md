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

### API Actions

- [x] List Rooms
- [x] See Room
- [x] Create Room
- [ ] Edit Room
- [ ] Delete Room
- [ ] Filter Rooms
- [ ] Add Room to Favourites
- [ ] Search By Coords
- [ ] Login
- [ ] Create Account
- [ ] See Favs
- [ ] See Profile
- [ ] Edit Profile
