## RideGroup Server
Server for [RideGroup](https://github.com/git-uname/ride_group/)
### Development
- Install Python 3.6+ and PostgreSQL 11.2+ (other PostgreSQL versions may work but are unsupported)
- Install Postgis
- `pip install -r requirements.txt`
- Create a PostgreSQL user and update DATABASES in `settings.py` accordingly
    - To use default DATABASES:
        - `CREATE DATABASE ridegroup;`
        - `CREATE USER ridegroup WITH PASSWORD "ridegrouppassword";`
        - `GRANT ALL PRIVILEGES ON DATABASE ridegroup TO ridegroupuser;`
    - Note that in order to run tests you will need to `ALTER USER [username] CREATEDB;` so the testing database can be created
- Temporarily make the  postgres user a superuser to migrate with `ALTER USER [username] WITH SUPERUSER;`
- `python manage.py makemigrations ridegroup` and `python manage.py migrate`
- Make the postgres user not superuser `ALTER USER [username] WITH NOSUPERUSER;`
- Download the Firebase Admin Private Key from the [Firebase Console](https://console.firebase.google.com) as `firebase.json`
