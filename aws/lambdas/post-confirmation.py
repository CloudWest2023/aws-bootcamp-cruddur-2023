import json
import psycopg2

def lambda_handler(event, context):
    user = event['request']['userAttributes']
    print(f"user: {user}")

    display_name = user['name']
    email = user['email']
    handle = user['preferred_username']
    cognito_user_id = user['sub']
    sql = f"""
            INSERT INTO users (
                display_name, 
                email,
                handle,     
                cognito_user_id
            ) 
            VALUES( %s, %s, %s, %s )
            """

    try:
        print('SQL Statement ----')
        print(sql)

        params = [
                display_name,
                email,
                handle,
                cognito_user_id,
        ]

        conn = psycopg2.connect(os.getenv('CONNECTION_URL'))
        cur = conn.cursor()
        cur.execute(sql, *params)
        conn.commit() 

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

    return event