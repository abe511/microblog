## a python blog app


#### Requirements:

* Python 3.10 or greater

* Postgres running locally on port 5432 (modify in `.env` file)

* Docker (for containerized version)

---

#### Run in containers:

open a terminal and cd to the project root dir:

for MacOS/Linux run:

```
make
```

on Windows run:

```
docker compose up
```

in a browser open

>http://127.0.0.1:8000/


for admin panel

>http://127.0.0.1:8000/admin


to remove the containers and images run 

`make clean`


#### Run the app:

0. clone the repo and cd into the project directory
1. rename `example.env` to `.env`
2. edit DB_PORT, DEV_DB_PORT and other variables according to your db server location
3. create `flask_db` database in your postgres server
4. create a virtual environment 
```
python3 -m venv venv
```

5. activate virtual environment
```
source venv/bin/activate
```
6. install dependencies

```
pip install -r requirements.txt
```

7. make sure that `FLASK_ENV` in `.env` file is set to `development` or `production`

8. start the app

```
flask run
```
9. in a browser open
>http://localhost:5000

10. to use admin panel go to 
>http://localhost:5000/admin
