# How to run locally:

1. Make sure you have you postgres running on your localhost and port 5434 (In case other port change path 
        app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/flask_db"
2. Run flask migration (flask db upgrade)
3. Run app.py
4. In case using shell. Use flask shell command