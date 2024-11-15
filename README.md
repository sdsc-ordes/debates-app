# Political Debates UI

## About

This is the GUI setup with docker compose for the political debates project
It contains the following services

- Minio: store for the original data
- Minio Client: mc cli tool for minio to perform the initial setup 
- Mongodb: store for metadata derived from the original data
- Solr: search engine that is fed with the latest derived metadata version from the mongodb
- Mongo Express: as convenient UI for the mongodb
- Dataloader: with fastapi as backend
- Frontend: frontend in Sveltekit, that has a videoplayer page and a search page: the videoplayer page allows to play videos along with their transcripts and edit transcripts and speaker info. The metadata can be edited and stored back to the mongodb as a new version.

## Docker compose setup

### Environment variables

The compose setup needs a `.env` file for secrets:

```bash
cp .env.dist .env
```

Then provide the following information in the `.env` file:

```bash
# SOLR settings
SOLR_SELECT_URL=http://proxy:8010/solr/debates/select
SOLR_BASE_URL=http://proxy:80/solr/debates/
SOLR_PATH=[your-path-to-solr-volume]

# Mongo Settings
MONGO_DB=debates
MONGO_VIDEO_COLLECTION=videos
MONGO_USER=[your-mongo-user]
MONGO_PASSWORD=[your-mongo-password]
MONGO_PATH=[your-path-to-mongo-volume]

# Mongo Express Settings
MONGO_EXPRESS_USER=admin
MONGO_EXPRESS_PASSWORD=test1234

# Minio Settings
S3_BUCKET_NAME=debates
S3_ACCESS_KEY=[your-minio-user]
S3_SECRET_KEY=[your-minio-password]
MINIO_PATH=[your-path-to-minio-volume]
```

### Docker Compose profiles

The docker compose setup uses profiles:

#### Local Development

```
docker-compose build
docker-compose up -d
```

This starts only the services but not frontend and backend: these can then be started separately
for development, see instructions in their README's

#### Docker Compose locally

```
docker-compose --profile compose build
docker-compose --profile compose up -d
```

Make sure the frontend is been build with the correct `.env` file in the frontend container.
In order to run with docker compose it needs the services in the urls for mongodb and dataloader:

```
SECRET_MONGO_URL=mongodb://[your-mongo-user]:[your-mongo-password]@mongodb-instance:27017/
PUBLIC_BACKEND_SERVER=http://dataloader:8000
```

#### Docker Compose on VM

```
docker-compose --profile vm build
docker-compose --profile vm up -d
```

### Loading data on first start up and later per video

Once the containers are running: you need to go into the dataloader container and load the data into mongodb and s3 initially. Once set up the date will be retained in the volumes.

#### Load data into S3:

this can be done manually via the minio ui:

- create a bucket `debates`
- set it to `public`
- load the following object keys per prefix `HRC_20220929`: 

```
HRC_20220929/HRC_20220929.srt
HRC_20220929/HRC_20220929.mp4
```

#### Load metadata into mongodb

```
python debates.py mongo-admin --delete
python debates.py mongo-admin --create
python debates.py s3-to-mongo HRC_20220929/HRC_20220929.srt HRC_20220929/HRC_20220929.yml
python debates.py mongo-get --all
```

```
[{'_id': ObjectId('6723a618e69de6600dc04597'),
  's3_prefix': 'HRC_20220929',
  'version_id': 'e472d26a-b343-4547-ac7d-cccfc5e890a7'},
```

#### Load metadata into Solr

```
python debates.py mongo-to-solr HRC_20220929 e472d26a-b343-4547-ac7d-cccfc5e890a7
```

# PROD urls

https://debates.swisscustodian.ch/solr/#/

https://debates.swisscustodian.ch/

To enter the shell for the initial dataloading:

```
docker exec -it debates-dataloader-1 sh
```

### Next Steps

- automize setup and dataloading per video
