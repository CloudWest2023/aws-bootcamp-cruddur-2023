-- this file was manually created.

INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
    ('Coding Vihuela', 'coding.vihuela', 'viuela@gmail.com', 'MOCK'),
    ('Coding Pinata', 'coding.pinata', 'pinata@gmail.com', 'MOCK');

    -- ('Mariachi in a Jar', 'mariachiinajar', 'MOCK'),
    -- ('Matryoshka in the Cloud', 'matryo', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'coding.vihuela' LIMIT 1),
        'Is the db on AWS Cloud connected?',
        current_timestamp + interval '10 day'
    ),
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'coding.pinata' LIMIT 1),
        'If you are seeing this message, then yes, it is connected!',
        current_timestamp + interval '10 day'
    )
    