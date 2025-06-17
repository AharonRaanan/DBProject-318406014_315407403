import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

DSN = f"dbname={os.getenv('DBNAME')} user={os.getenv('USER')} password={os.getenv('PASSWORD')} host={os.getenv('HOST')} port={os.getenv('PORT')}"

@contextmanager
def get_conn(cur_dict=False):
    conn = psycopg2.connect(dsn=DSN)
    try:
        yield conn.cursor(cursor_factory=RealDictCursor) if cur_dict else conn.cursor()
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
