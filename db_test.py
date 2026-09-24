import psycopg

connection = psycopg.connect(
    "dbname=takeoff_db user=takeoff_app password=takeoff_dev_password host=localhost"
)

print("Database connection successful!")

connection.close()