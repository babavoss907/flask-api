# Flask API 

- Flask micro service to CRUD.

- Creating MySQL in a docker container.

- Basic JWT auth token is set for 30 min

- Using Pydantic/OpenAPI for validation and documentaion.

- No Frontend


1. Clone repo

```
$ git clone https://github.com/babavoss907/flask-api.git
```

```
$ cd flaskmicro
```

2. Create Shell, install dependencies/requirements.

```
$ pipenv shell
```

```
$ pip install -r requirements.txt
```

3. Create Database in Docker Container in detached

```
$ docker-compose up -d
```

3. create table

- enter docker shell
```
$ docker exec -it flaskmicro_db_1 bash
```
- enter MySQL
```
$ mysql -u root -p
```

- password = "root"

```
$ use local_db
```

```
$ CREATE TABLE `authors` (
	`id` INT(11) NOT NULL AUTO_INCREMENT, `first_name` VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci', `last_name` VARCHAR(50) NOT NULL COLLATE 'utf8_unicode_ci', `email` VARCHAR(100) NOT NULL COLLATE 'utf8_unicode_ci', `birthdate` DATE NOT NULL,
	`added` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`), UNIQUE INDEX `email` (`email`)
)
COLLATE='utf8_unicode_ci'
ENGINE=InnoDB;
```

4. Start Application/ source .env

```
$ source .env
```

```
$ flask run
```

5. Visit App Docs
http//:127.0.0.1:5000/flask-micro-service

6. Get Access Token

- flask-miro/auth
- "Try it out"
username = "root"
password = "admin"
- "Execute"
- Copy access token

7. Authenticate
- click "Authorize"
- paste token

8. Insert Authors