aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "Harry Styles"}, 
        "SongTitle": {"S": "As it was"}, 
        "AlbumTitle": {"S": "As It Was"}}' \
    --return-consumed-capacity TOTAL  

aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "Arctic Monkeys"}, 
        "SongTitle": {"S": "505"}, 
        "AlbumTitle": {"S": "Favourite Worst Nightmare"}}' \
    --return-consumed-capacity TOTAL  

aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "The xx"}, 
        "SongTitle": {"S": "Crystalised"}, 
        "AlbumTitle": {"S": "Crystalised"}}' \
    --return-consumed-capacity TOTAL  


aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "Alec Benjamin"}, 
        "SongTitle": {"S": "Let Me Down Slowly"}, 
        "AlbumTitle": {"S": "Let Me Down Slowly"}}' \
    --return-consumed-capacity TOTAL  