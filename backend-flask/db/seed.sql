-- this file was manually created.

INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
    -- ('Coding Vihuela', 'coding.vihuela', 'viuela@gmail.com', 'MOCK'),
    -- ('Coding Pinata', 'coding.pinata', 'pinata@gmail.com', 'MOCK');

    -- ('Mariachi in a Jar', 'mariachiinajar', 'MOCK'),
    -- ('Matryoshka in the Cloud', 'matryo', 'MOCK');

    ('Mariachi in a Jar', 'mariachiinajar', 'mariachiinajar@gmail.com', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'mariachiinajar' LIMIT 1),
        'Currently fighting through Week 5!',
        current_timestamp + interval '10 day'
    );
    