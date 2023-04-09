-- this file was manually created.

INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
    ('Coding Vihuela', 'coding.vihuela', 'MOCK'),
    ('Coding Pinata', 'coding.pinata', 'MOCK');

    -- ('Mariachi in a Jar', 'mariachiinajar', 'MOCK'),
    -- ('Matryoshka in the Cloud', 'matryo', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'coding.vihuela' LIMIT 1),
        'coding.vihuela is a clone 1 of Mariachi in a Jar',
        current_timestamp + interval '10 day'
    ),
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'coding.pinata' LIMIT 1),
        'coding.pinata is an alternate developer 2 of Mariachi in a Jar',
        current_timestamp + interval '10 day'
    )
    