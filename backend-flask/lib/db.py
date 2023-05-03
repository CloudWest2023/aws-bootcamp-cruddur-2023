from psycopg_pool import ConnectionPool
import os, sys, re
from flask import current_app as app

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..'))
sys.path.append(parent_path)
from utils.bcolors import *


class db:

    def __init__(self):
        self.init_pool()

    # Create a PostgreSQL pool connection
    def init_pool(self):
        printh("INIT_POOL() in action ...")

        psql_url = os.getenv("URL_PROD")
        printc(f"   psql_url: {psql_url}")
        db_name = os.getenv("DB_NAME_PROD")
        printc(f"   db_name: {db_name}")

        connection_url = str(f"{psql_url}{db_name}")
        printc(f"   connection_url: {connection_url}")

        if db_name in connection_url:
            printc(f"    Connecting to: AWS RDS production db - {db_name}")
        self.pool = ConnectionPool(connection_url)
        printc(f"    {self.pool}")
        printh(f"    ... INIT_POOL() complete\n")

    
    # File opener. 
    # Reads in the file and returns the content. 
    def template(self, *args):
        printh(f"DB.TEMPALTE() in action ....")

        printc(f"   app.root_path: {app.root_path}")
        PATH = list((app.root_path, 'bin', 'rds', 'sql') + args)
        PATH[-1] = f"{PATH[-1]}.sql"
        printc(f"   PATH: {PATH}")

        TEMPLATE_PATH = os.path.join(*PATH)
        printc(f"    SQL TEMPLATE-[{TEMPLATE_PATH}]\n")

        with open(TEMPLATE_PATH, 'r') as f:
            template_content = f.read()

        printh(f"    ... DB.TEMPALTE() complete\n")    
            
        return template_content


    def load_sql(self):
        pass

    
    # Commit data such as an insert
    # Be sure to check for 'RETURNING' in all uppercases. 
    def query_commit(self, sql, params={}):
        printh("QUERY_COMMIT() with returning id ...", sql, params)

        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql)

        try:
            with self.pool.connection() as conn:
                cur = conn.cursor()
                cur.execute(sql, params)

            if is_returning_id:
                returning_id = cur.fetchone()[0]
                printc("returning_id: ")
            else: 
                printc("No match found.")

            conn.commit()

            if is_returning_id:
                return returning_id

        except Exception as err:
            print("Error handling in action------------")
            self.print_err(err)
        
        printh("    ... QUERY_COMMIT() complete\n")


    # Simple query
    def query_value(self, sql, params={}):
        printh("QUERY_VALUE() in action ...")
        print_sql('value', sql=sql, params=params)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                json = cur.fetchone()
                return json[0]
        
        printh("    ... QUERY_VALUE() complete\n")


    # Return a json object
    def query_json_object(self, sql, params={}):
        print_sql('json', sql)
        wrapped_sql = self.query_wrap_object(sql)
        
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()
                return json[0]
    

    # Return an array of json object
    def query_json_array(self, sql, params={}):
        print_sql(title="Array", sql=sql)

        wrapped_sql = self.query_wrap_json_array(sql)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                # this will return a tuple 
                # the first field being the data
                json = cur.fetchone()

                print("=====================PRINT ROW======================")
                for dictionary in json[0]:
                    for key, value in dictionary.items():
                        print(f"{key}: {value}")
                print("\n\n")

                return json[0]


    def query_wrap_json_object(self, template):
        print_sql("Object", sql)

        sql = f"""
            (SELECT COALESCE(row_to_json(object_row), '{{}}'::json) 
                FROM ({template}) object_row);
            """
        print(f"template: {template}")
        print(f"sql: {sql}")
        return sql


    def query_wrap_json_array(self, template):
        printh("QUERY_WRAP_JSON_ARRAY() in action ...")
        sql = f"""
            (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))), '[]'::json) 
                FROM ({template}) array_row);
            """
        print(f"template: {template}")
        print(f"sql: {sql}")
        return sql


    def print_err(self, err):
        # Get details about the exception.
        err_type, err_obj, traceback = sys.exc_info()

        # Get the line number when exception occurred.
        line_num = traceback.tb_lineno

        # Print the connect() error
        print(f"\npsycopg2 ERROR: {err} on line number: {line_num}")
        print(f"psycopg2 traceback: {traceback} -- type: {err_type}")

        # psycopg2 extensions.Diagnostics object attribute
        print(f"\nextensions.Diagnostics: {err}") # err.diag

        # Print the pgcode and pgerror exceptions
        # print(f"pgerror: {err.pgerror}")
        # print(f"pgcode: {err.pgcode}\n")

db = db()