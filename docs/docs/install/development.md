# Development setup

In the development setup the docker compose file `docker-compose.dev.yml` is used to run only the databases as services. The dataloader and frontend are then run locally outside of docker.

## Environment Variables for docker compose

The env variables are similar to the [compose setup](compose.md): you have to set:

- [environment for the debates app](compose.md#environment-variables-for-debates-app)

## Docker compose

The development setup has it's own docker compose file `docker-compose.dev.yml`.

```
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up -d
```

## Setup the dataloader backend

The backend needs now its own `backend.env` as follows:

```
# External Service settings:
# must match the docker compose settings for the services
SOLR_URL=http://localhost:8010/solr/debates/
S3_ACCESS_KEY=
S3_SECRET_KEY=

# Use this for local
API_HOST="127.0.0.1"
MONGO_URL=
S3_SERVER=http://localhost:9000
FRONTEND_SERVER=http://localhost:5173

# Use this for compose
S3_FRONTEND_BASE_URL=

# this is for the PROD S3
PROD_S3_BUCKET_NAME=
PROD_S3_ACCESS_KEY=
PROD_S3_SECRET_KEY=
PROD_S3_REGION_NAME=
```

The `PROD_S3_*` are there for the transfer of data from the Pipeline S3 to the App S3.

After you have [loaded the data into the App S3](../architecture/dataloader.md), you can build the backend and then serve the backend api:

```
cd dataloader
rye install
rye sync
source .venv/bin/activate
python src/debates.py serve
```

## Setup of the frontend

You need to adapt the `frontend/.env`:

```
# in local dev setup
#PUBLIC_BACKEND_SERVER=http://0.0.0.0:8000
```

After that install and mount the frontend with:

```
cd frontend
pnpm install
pnpm dev
```

The frontend should now be up and running and tell you the url where it is available

## Load data

See [compose setup](compose.md#load-data)
