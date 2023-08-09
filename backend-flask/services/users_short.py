from lib.db import db

class UsersShort: 
    def run(handle):
        sql = db.template('users', 'short')
        results = db.query_json_object(sql, {
            'handle': handle
        })
        return results