# ESA Hubble

Djangoplicity CMS for the ESA Hubble Project (https://www.spacetelescope.org/)

## Requirements

- Docker
- Docker Compose

## Development

### Cloning the repository

In your terminal run the command:

```` 
git clone https://gitlab.com/esahubble/esahubble.git
````

### Running the project

All the configuration to start the project is present in the docker compose files and Dockerfile,
then at this point a single command is required to download all the dependencies and run the project:

```` 
docker compose up
````

> The previous command reads the config from docker-compose.yml and docker-compose.override.yml, because of the naming convention of docker-compose

When the process finishes, the CMS will be available at *`localhost:8000`*

To stop containers press:

```
CTRL + C
```

If the dependencies change, you should recreate the docker images and start the containers again with this command:

```` 
docker compose up --build
````

### Additional commands

Inside the `Makefile` there are multiple command shortcuts, they can be run in UNIX systems like this:

```
make <command-name>
```

E.g.

```
make migrate
```

> In windows you can just copy and paste the related command

### The demo seed

The project contains a _demo seed_ that can be loaded in order to populate example data to the database, to load the demo data run the following command while the containers are running:

```
docker exec -it hubble ./manage.py loaddata demo
```

or

```
make demofixture
```

### Accessing Administration

The django admin site of the public site can be accessed at `localhost:8000/admin`

By default the development configuration creates a superuser with the following credentials:

```
Username: admin
Password: admin
```

## Deployment and Production

### Prerequisites

The production environment requires certain configuration before deploying the docker containers, such as the database,
the Nginx reverse proxy and the volumes.

#### Storage Volume

The system requires a big amount of storage size for the media archive, therefore the containers are configured to store
them in a volume with enough size, currently the big volume should be located here:

```
/mnt/volume_fra1_01
```

And the subdirectory required by the project is:

```
/mnt/volume_fra1_01/web
```

**IMPORTANT:** The volume's subdirectory owner should be the same user as in the docker containers, currently `hubbleadm`,
the GUI and UID should be `2000`, otherwise the containers won't have enough permissions to read/write to the volume,
then the following commands may be needed:

```
sudo groupadd -g 2000 hubbleadm
sudo useradd -u 2000 -g hubbleadm --create-home hubbleadm
sudo mkdir /mnt/volume_fra1_01/web/
sudo chown -R hubbleadm:hubbleadm /mnt/volume_fra1_01/web/
```
> This command: `sudo chown -R hubbleadm:hubbleadm /mnt/volume_fra1_01/web/` may be required after the containers startup again so that the permissions of the created volumes are set correctly

#### Environment variables

The system is configured using environment variables, you can either set them in the shell or in a file called `.env`
located next to the `docker-compose.yml` file, the content of the `.env` file should look like this:

```
RABBITMQ_USER=my_user
RABBITMQ_PASS=my_password
```

> **NOTE:** Shell environment variables have a higher priority than the `.env` file 

The following is the list of environment variables that are required or optional before deploying the system:

| Variable | Description | Required | Default |
| :--- | :--- | :---: | :--- |
| `DJANGO_SECRET_KEY` | Key used by Django for tokens like CSRF and cookies, it can be any secret key but it's recommended to generate it using https://djecrety.ir/ | **yes** | *None* |
| `RABBITMQ_USER` | Custom username for the Rabbitmq broker | **yes** | *None* |
| `RABBITMQ_PASS` | Custom password for the Rabbitmq broker | **yes** | *None* |

#### Backing services

As expected in a Twelve Factors App the following services needs to be configured using environment variables as well:

| Service | Environment variable | Value | Example |
| :--- | :---: | :--- | :--- |
| Postgres Database | `DATABASE_URL` | `postgresql://<user>:<pass>@<host>:<port>/<dbname>` | `postgresql://admin:1234@hubble-db.com:5432/hubble?sslmode=require` |

#### SSH Key (CDN77)

In order to push files to the CDN storage the system uses `rsync` which relies on an SSH connection, therefore an SSH Key must be added outside the container in:
```
config/.ssh
```

In the server use the following command to do so:
```
ssh-keygen -f /path/to/config/.ssh/id_rsa
```
> *IMPORTANT*: Do not add a passphrase to the key, otherwise the application won't be able to use it

Give the correct owner to the files:
```
sudo chown -R hubbleadm:hubbleadm config/.ssh/
```

Finally configure the public key in the CDN Storage by following the next steps
- https://client.cdn77.com/support/knowledgebase/cdn-resource/how-to-use-rsync-without-password

### Deployment

When having all the prerequisites, clone the repository in the server, then deploy the containers with the command:
```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Or if `make` is installed:
```
make prod-up-build
```

That's it!. The system is available in the port `8000`, and can be proxied using `Nginx`

#### Additional commands 

In case of new updates pull the commits from the repository and run the same command of the previous step. 

If the updates only changes the docker configuration just run:
```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```
or
```
make prod-up
```

To start the containers displaying the startup logs:
```
docker compose -f docker-compose.yml -f docker-compose.prod.yml up
```
or
```
make prod-up-attached
```
> **NOTE:** The previous command attach the process to the terminal, 
then pressing `Ctrl + C` is required to continue using it, but it also stops the containers

#### Troubleshooting

Most of the problems can be found while reading the docker logs of each container:
```
docker logs <container name>
```

Examples:
```
docker logs hubble
docker logs hubble-celery
docker logs hubble-broker
```
