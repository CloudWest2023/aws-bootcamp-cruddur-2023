SELECT
    user.uuid,
    user.handle,
    user.display_name
FROM users
WHERE 
    users.handle = %(handle)s