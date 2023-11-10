## a python blog app

> Checkout [**this demo**](https://microblog-fizz.onrender.com/) 

* *deployed from `deployment` branch, runs on Gunicorn*


#### Requirements:

* Python 3.10 or greater

* Postgres running locally on port 5432 (modify `.env` file)

* Docker (for containerized version)

---

#### Run in containers:

open a terminal and cd to the project root dir:

on MacOS/Linux run:

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


to remove containers and images run 

`make clean`


#### Run the app:

1. `git clone` the repo and `cd` into the project directory
2. rename `.env.example` to `.env`
3. modify `DEV_DB_PORT` and other variables according to your db server location
4. create `flask_db` database in your Postgres server
5. create a virtual environment 
```
python3 -m venv venv
```

6. activate virtual environment
```
source venv/bin/activate
```
7. install dependencies

```
pip install -r requirements.txt
```

8. make sure that `FLASK_ENV` in `.env` file is set to `development` mode

* *set `FLASK_ENV=test` to use in-memory `SQLite` database*

9. start the app

```
flask run
```
10. in a browser open
>http://localhost:5000

11. to use admin dashboard go to 
>http://localhost:5000/admin
