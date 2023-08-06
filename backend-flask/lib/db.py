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
        printh("db.init_pool() ...")

        connection_url = os.getenv("AWS_RDS_POSTGRES_ENDPOINT")
        printc(f"   connection_url: {connection_url}")

        self.pool = ConnectionPool(connection_url)
        printc(f"    {self.pool}")
        printh(f"    ... db.init_pool()\n")

    
    # File opener. 
    # Reads in the file and returns the content. 
    def template(self, *args):
        printh(f"db.template() ...")

        printc(f"app.root_path: {app.root_path}")
        PATH = list((app.root_path, 'bin', 'rds', 'sql') + args)
        PATH[-1] = f"{PATH[-1]}.sql"
        printc(f"PATH: {PATH}")

        TEMPLATE_PATH = os.path.join(*PATH)
        printc(f"SQL TEMPLATE-[{TEMPLATE_PATH}]\n")

        with open(TEMPLATE_PATH, 'r') as f:
            template_content = f.read()

        printh(f"    ... db.template()\n")    
            
        return template_content


    def load_sql(self):
        pass

    
    # Commit data such as an insert
    # Be sure to check for 'RETURNING' in all uppercases. 
    def query_commit(self, sql, params={}):
        printh("db.query_commit() ...")

        pattern = r"\bRETURNING\b"
        is_returning_id = re.search(pattern, sql) # params

        try:
            with self.pool.connection() as conn:
                cur = conn.cursor()
                cur.execute(sql, params)

            if is_returning_id:
                returning_id = cur.fetchone()[0]
                printc("    returning_id: ")
            else: 
                printe("    No match found.")

            conn.commit()

            if is_returning_id:
                return returning_id

        except Exception as err:
            printe("    query_commit().Exception in action...")
            self.print_err(err)
        
        printh("    ... db.query_commit()\n")


    # Simple query
    def query_value(self, sql, params={}):
        printh("db.query_value() ...")
        print_sql('value', sql=sql, params=params)
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                json = cur.fetchone()
                return json[0]
        
        printh("    ... db.query_value()\n")


    # Return a json object
    def query_json_object(self, sql, params={}):
        printh("db.query_json_object() ...")
        print_sql('json', sql)
        wrapped_sql = self.query_wrap_json_object(sql)
        
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(wrapped_sql, params)
                json = cur.fetchone()

                printh("    ... db.query_json_object()")

                return json[0]
    

    # Return an array of json object
    def query_json_array(self, sql, params={}):
        printh("db.query_json_array() ...")
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
                printh("    ... db.query_json_array().")

                return json[0]


    def query_wrap_json_object(self, template):
        sql = f"""
        (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
        {template}
        ) object_row);
        """

        printh("db.query_wrap_json_object() in action ...")
        print_sql("Object", sql)

        sql = f"""
            (SELECT COALESCE(row_to_json(object_row), '{{}}'::json) 
                FROM ({template}) object_row);
            """
        print(f"    template: {template}")
        print(f"    sql: {sql}")

        printh("    ... db.query_wrap_json_object() complete.")

        return sql


    def query_wrap_json_array(self, template):
        printh("db.query_wrap_json_array() in action ...")
        sql = f"""
            (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))), '[]'::json) 
                FROM ({template}) array_row);
            """
        print(f"template: {template}")
        print(f"sql: {sql}")
        
        printh("    ... db.query_wrap_json_array() complete.")
        
        return sql


    def print_err(self, err):
        printh("db.print_err() ...")
        # Get details about the exception.
        err_type, err_obj, traceback = sys.exc_info()

        # Get the line number when exception occurred.
        line_num = traceback.tb_lineno

        # Print the connect() error
        print(f"db.print_err() psycopg2 ERROR: {err} on line number: {line_num}")
        print(f"db.print_err() psycopg2 traceback: {traceback} -- type: {err_type}")

        # psycopg2 extensions.Diagnostics object attribute
        print(f"db.print_err() extensions.Diagnostics: {err}") # err.diag
        printh("    ... db.print_err()")    
        
        # Print the pgcode and pgerror exceptions
        # print(f"pgerror: {err.pgerror}")
        # print(f"pgcode: {err.pgcode}\n")

db = db()