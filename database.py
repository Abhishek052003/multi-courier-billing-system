import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="billing_project",
        user="postgres",
        password="abhi@2003",
        port="5432"
    )