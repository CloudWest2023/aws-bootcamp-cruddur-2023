-- this file was manually created.

INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
    ('Mariachi in a Jar', 'mariachiinajar', 'MOCK'),
    ('Matryoshka in the Cloud', 'matryo', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'mariachiinajar' LIMIT 1),
        'This was imported as seed data!',
        current_timestamp + interval '10 day'
    )