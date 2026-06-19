import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2 import pool

connection_pool = psycopg2.pool.ThreadedConnectionPool(
    minconn=2,
    maxconn=10,
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT", 5432),
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
)

def get_conn():
    return connection_pool.getconn()

def release_conn(conn):
    connection_pool.putconn(conn)

def init_db():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                role VARCHAR(100),
                department VARCHAR(100),
                salary NUMERIC
            );
        """)
        cur.execute("SELECT COUNT(*) FROM employees;")
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute("""
                INSERT INTO employees (name, role, department, salary) VALUES
                ('Alice Johnson', 'Engineer', 'Engineering', 95000),
                ('Bob Smith', 'Manager', 'Operations', 105000),
                ('Carol White', 'Designer', 'Product', 88000),
                ('David Brown', 'Analyst', 'Finance', 82000),
                ('Eva Green', 'DevOps', 'Engineering', 98000),
                ('Frank Black', 'Scrum Master', 'Engineering', 91000),
                ('Grace Lee', 'HR Specialist', 'HR', 75000),
                ('Henry Wilson', 'Sales Lead', 'Sales', 87000),
                ('Iris Moore', 'Data Scientist', 'Engineering', 102000),
                ('Jake Taylor', 'QA Engineer', 'Engineering', 80000);
            """)
        conn.commit()
        cur.close()
    finally:
        release_conn(conn)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    connection_pool.closeall()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/employees")
def get_employees():
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, name, role, department, salary FROM employees ORDER BY id;"
        )
        rows = cur.fetchall()
        cur.close()
        employees = [
            {
                "id": r[0],
                "name": r[1],
                "role": r[2],
                "department": r[3],
                "salary": float(r[4]),
            }
            for r in rows
        ]
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        release_conn(conn)
