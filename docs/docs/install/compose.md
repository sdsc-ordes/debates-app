# Compose setup

## Clone the repo:

```
git clone git@github.com:sdsc-ordes/debates-app.git
cd debates-app
git submodule update --init
```

## Environment variables for Debates App

```
cp .env.dist .env
```

You need to set the following credentials:

- **App S3**: `[ACCESS_KEY]`, `[SECRET_KEY]`
- **Mongo DB**: `[MONGO_USER]`, `[MONGO_PASSWORD]`
- **Mongo Express**: `[MONGO_EXPRESS_USER]`, `[MONGO_EXPRESS_PASSWORD]`

You also need a directory for volumes:

```
debates
├── debates-app
└── data
    ├── minio
    ├── mongo
    └── s3
```

Save the pathes:

- `[PATH_MINIO]`
- `[PATH_MONGO]`
- `[PATH_S3]`

Then the `.env` file is filled as follow:

```
# Credentials
# s3
S3_ACCESS_KEY=ACCESS_KEY]
S3_SECRET_KEY=[SECRET_KEY]
# Mongo DB
MONGO_USER=[MONGO_USER]
MONGO_PASSWORD=[MONGO_PASSWORD]
# Mongo Express
MONGO_EXPRESS_USER=[MONGO_EXPRESS_USER]
MONGO_EXPRESS_PASSWORD=[MONGO_EXPRESS_PASSWORD]

# volumes to store the data of services in docker compose
SOLR_PATH=[PATH_SOLR]
MONGO_PATH=[PATH_MONGO]
MINIO_PATH=[PATH_MINIO]
```

## Environment Variables for frontend

The frontend is build with [Sveltekit](https://svelte.dev/) and also a environment variable:

```
cd frontend
sp .env.dist .env
```

The `.env` file of the frontend should look like this:

```hl_lines="2"
# for docker compose setup
PUBLIC_BACKEND_SERVER=http://dataloader:8000
```

The url connects it to the backend.

## Build docker compose

Now you are ready to build and run docker compose

```
docker compose -f docker-compose.compose build
docker compose -f docker-compose.compose up -d
```

Now that the containers are running, enter the dataloader container

# Load data

This step describes the initial data loading

```
docker exec -it debates-dataloader-1 sh
```
