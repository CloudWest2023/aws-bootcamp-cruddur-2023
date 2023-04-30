-- this file was manually created.

INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
    -- ('Coding Vihuela', 'coding.vihuela', 'viuela@gmail.com', 'MOCK'),
    -- ('Coding Pinata', 'coding.pinata', 'pinata@gmail.com', 'MOCK');

    -- ('Mariachi in a Jar', 'mariachiinajar', 'MOCK'),
    -- ('Matryoshka in the Cloud', 'matryo', 'MOCK');

    ('Billy Paigh', 'billypaigh', 'billypaigh@gmail.com', 'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'coding.vihuela' LIMIT 1),
        'Currently fighting through Week 5!',
        current_timestamp + interval '10 day'
    ),
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'coding.pinata' LIMIT 1),
        'I came along way to fight "Week 5 Implement Conversations with DynamoDB"!!',
        current_timestamp + interval '10 day'
    )
    