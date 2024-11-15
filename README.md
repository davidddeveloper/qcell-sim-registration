# qcell-sim-registration
Register your qcell sim.

## Notes on dockerization

### Setting up the docker environment
#### Install docker
    sudo snap install docker

    sudo service docker status  # check if docker is running
    
    sudo service docker stop  # stops a docker service
    sudo service docker start  # starts a docker service

    sudo docker pull hello-world
    sudo docker run hello-world


#### Creating the docker files
create a docker-compose.yml file for this project in the following structure

    version: '3'
    services:
    db:
        image: mysql:8
        container_name:
        environment:
        MYSQL_ROOT_PASSWORD:
        MYSQL_DATABASE:
        MYSQL_USER:
        MYSQL_PASSWORD:
        ports:
        - "3306:3306"
        networks:
        - default

    web:
        build: .
        container_name:
        volumes:
        - ./staticfiles:/app/staticfiles # for serving static files outside docker in the host manchine. Change this to whatever directory you're collecting staticfiles to
        ports:
        - "8000:8000"
        environment:
        DB_NAME:
        DB_USER:
        DB_PASSWORD:
        DB_HOST:
        MySQL service
        DB_PORT:
        depends_on:
        - db
        networks:
        - default

    networks:
    default:
        driver: bridge


#### Basic docker commands
    sudo docker --version  # To check the currently installed version of docker.

    sudo docker pull hello-world  # To download an image from hub.docker.com

    sudo docker images  # Shows all the currently installed docker images

    sudo docker run hello-world  # To run the docker image. This will pull and run the image if it is not available locally.

    sudo docker run --names helloworld hello-world  # To run a docker container and bind it with a specific name.

    sudo docker run -d nginx  # To run a docker container in detached mode (in background).

    sudo docker ps  # Shows all the currently running docker containers their status, ids and names

    sudo docker stop <container_id>  # To stop a running docker container

    sudo docker stop <container_name>  # To stop a running docker container

    sudo docker start <container_name or container_id>  # To start a stopped docker container


#### Basic docker-compose commands
ensure that you have a docker-compose.yml file with the correct information as stated above.

    sudo docker-compose build  # builds (install, compile) the docker image(s) specified in the docker-compose.yml file

    sudo docker-compose up  # run the docker images in docker-compose.yml file

    sudo docker-compose up  # run the docker images in docker-compose.yml file in detatch mode

    sudo docker-compose up -d --build  # builds and run the docker images in docker-compose.yml file in detatch mode

    sudo docker-compose up -d --build <service/container_name>  # builds and run a specific docker container in the docker-compose.yml file.

    sudo docker-compose down  # stops the currently docker images in the docker-compose.yml file

    sudo docker-compose stop <container/service_name>  # stops a specific docker container in the docker.yml file

    sudo docker-compose down -v  #  remove the volumes associated with the services. Like persisted database

    sudo docker-compose rm <service/container_name>  # removes stop containers. Do this so you can rerun containers with the same service/container_name

    sudo docker-compose exec <container/service_name> <command you want to run>  # allows you to execute a command inside a container

    sudo docker-compose exec web bash  # example of the docker command above. Opens a bash inside the web docker container

    sudo docker-compose logs <container/service_name>  # shows the logs output by a specific service or docker container.

#### Shipping our python-django application to production. (qcell-sim-registration)
Pull the repository on the server where you want to deploy this branch (git checkout dockerized_app)

##### STEP 1: Create a Dockerfile in the root repo
The [Dockerfile](./Dockerfile) is already created and can be found in the root repository (same as where this README is)

##### STEP 2: Create a .env file in sim_registration/
Passed the correct information in the .env in the django-app in sim_registration in the following structure

    SECRET_KEY = ""  # SECRET_KEY for django
    JWT_SECRET_KEY = ""  # JWT_SECRET_KEY for django-jwt

    # Note that the values you passed here should correspond with what is in the docker-compose.yml file

    DB_NAME = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_HOST = "david-mysql-container"  # replace with the docker mysql container/service name (not 12.0.0.1)
    DB_PORT = "3306"  # replace with the correct port


##### STEP 3: Create the docker-compose.yml file
Same as the one above with the correct information passed in. example

    version: '3'
    services:
    db:
        image: mysql:8
        container_name: david-mysql-container
        environment:
        MYSQL_ROOT_PASSWORD:
        MYSQL_DATABASE:
        MYSQL_USER:
        MYSQL_PASSWORD:
        ports:
        - "3306:3306"
        networks:
        - default

    web:
        build: .
        container_name:
        volumes:
        - ./staticfiles:/app/staticfiles # for serving static files outside docker in the host manchine. Change this to whatever directory you're collecting staticfiles to
        ports:
        - "8000:8000"
        environment:
        DB_NAME:
        DB_USER:
        DB_PASSWORD:
        DB_HOST:
        MySQL service
        DB_PORT:
        depends_on:
        - db
        networks:
        - default

    networks:
    default:
        driver: bridge

As you can see from above we are building too images a database and a web_server which is our django application.
Note that the

    DB_NAME:
    DB_USER:
    DB_PASSWORD:
    DB_HOST:
    DB_PORT:
    MYSQL_ROOT_PASSWORD:
    MYSQL_DATABASE:
    MYSQL_USER:
    MYSQL_PASSWORD:
SHOULD CORRESPOND WITH WHAT IS IN THE .env file

##### STEP 4: Build the images 🦾

    sudo docker-compose build

check if the images have been build

    sudo docker-compose images

##### STEP 4: Let's deploy 🚀
after setting up everything correctly. Run

    sudo docker-compose up -d

##### Additional Information
If you're setting nginx to proxy pass the request to the docker django application running on port 8000, Ensure to server static files like so

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000/;  # Change this to your application port
    }

    location /static/ {
        alias /home/davidconteh/qcell-sim-registration/staticfiles/;  # Path inside the container
        try_files $uri $uri/ =404;
    }

Optionally: to push an image to hub.docker.com

    sudo docker login --username davidconteh  # whoever the user is.

    sudo docker my-django-app:latest davidconteh/davidconteh-private:latest  # or whatever the repository is.

    docker push davidconteh/davidconteh-private:latest  # or whatever the repository is.
