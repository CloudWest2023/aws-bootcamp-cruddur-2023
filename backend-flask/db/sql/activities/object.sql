SELECT 
    activities.uuid,
    users.display_name,
    users.handle,
    acitvities.message,
    acitvities.created_at,
    acitvities.expires_at
FROM public.activities
INNER JOIN public.users ON users.uuid = activiites.user_uuid
WHERE 
    activities.uuid = %(uuid)s