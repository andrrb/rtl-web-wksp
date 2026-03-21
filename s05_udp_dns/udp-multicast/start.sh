# @echo off
# set DIR=C:\Users\Lenovo\OneDrive\Desktop\Seminar 5\udp-broadcast
# cd /d %DIR%

# REM Check if there are any containers or images for this project
# docker ps -a --filter "label=com.docker.compose.project=udp-broadcast" grep -c "udp-broadcast"'
# docker images | grep -c "udp-broadcast"'

# if %CONTAINERS%==0 if %IMAGES%==0 (
    # echo Building Docker images...
    # docker-compose build
# ) else (
    # echo Build already exists, skipping build.
# )

docker-compose up -d server

docker-compose logs -f server
docker-compose run --rm --service-ports client1 python client.py Alice
docker-compose run --rm --service-ports client2 python client.py Bob
docker-compose run --rm --service-ports client3 python client.py Charlie
