-- this file was manually created.

-- INSERT INTO public.users (display_name, handle, email, cognito_user_id)
-- VALUES
    -- ('Coding Vihuela', 'coding.vihuela', 'viuela@gmail.com', 'MOCK'),
    -- ('Coding Pinata', 'coding.pinata', 'pinata@gmail.com', 'MOCK');

    -- ('Mariachi in a Jar', 'mariachiinajar', 'MOCK'),
    -- ('Matryoshka in the Cloud', 'matryo', 'MOCK');

    -- ('Mariachi in a Jar', 'mariachiinajar', 'mariachiinajar@gmail.com', 'MOCK');
    -- ('Clouds of Things', 'clouds.of.things', 'cloudsofthings@gmail.com', 'MOCK');


INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
    (
        (SELECT uuid FROM public.users WHERE users.handle = 'mariachiinajar' LIMIT 1),
        'for week 8 - Implement Users Profile Page - seeding more data to test Profile page user data!!!',
        current_timestamp + interval '10 day'
    ),
        (
        (SELECT uuid FROM public.users WHERE users.handle = 'mariachiinajar' LIMIT 1),
        'for week 8 - My app is full of errors but I will get through this!',
        current_timestamp + interval '7 day'
    ),
        (
        (SELECT uuid FROM public.users WHERE users.handle = 'mariachiinajar' LIMIT 1),
        'for week 8 - More test data',
        current_timestamp + interval '5 day'
    );
    