SELECT
    users.uuid,
    users.handle,
    users.display_name
FROM users
WHERE 
    users.handle = %(handle)s