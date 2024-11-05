# Political Debates UI

## About

This is the GUI setup with docker compose for the political debates project
It contains the following services

- S3: store for the original data
- Mongodb: store for metadata derived from the original data
- Solr: search engine that is fed with the latest derived metadata version from the mongodb
- Mongo Express as convenient UI for the mongodb
- Dataloader: loads the original data into both Mongodb and Solr
- Frontend: frontend in Sveltekit, that has a videoplayer page and a search page: the videoplayer page allows to play videos along with their transcripts and edit transcripts and speaker info, that can be stored back to the mongodb as a new version of the metadata

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

# Input Files
VIDEO_INPUT="HRC_20220328.mp4"
SUBTITLES_INPUT="HRC_20220328.srt"
```

### Compose for dev and prod

There are three docker compose files:

- docker-compose.yml: common setup for dev and prod
- docker-compose.dev.yml: setup for dev
- docker-compose.prod.yml: setup for prod

Setup dev environment:

```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Set up on VM for publicly available prototype:

```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml build
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### Loading data

Once the containers are running: you need to go into the dataloader container and load the data into mongodb and s3 initially. Once set up the date will be retained in the volumes.

```
python debates.py mongo-admin --delete
python debates.py mongo-admin --create
python debates.py s3-to-mongo HRC_20220929/HRC_20220929.srt HRC_20220929/HRC_20220929.yml
python debates.py s3-to-mongo HRC_20220328/HRC_20220328.srt HRC_20220328/HRC_20220328.yml
python debates.py mongo-get --all
```

```
[{'_id': ObjectId('6723a618e69de6600dc04597'),
  's3_prefix': 'HRC_20220929',
  'version_id': 'e472d26a-b343-4547-ac7d-cccfc5e890a7'},
 {'_id': ObjectId('6723a62ac7f43009789b670f'),
  's3_prefix': 'HRC_20220328',
  'version_id': '3e7c8f90-f0ee-4f5d-a7dc-055f52966b62'}]
```

```
python debates.py mongo-to-solr HRC_20220328 3e7c8f90-f0ee-4f5d-a7dc-055f52966b62
python debates.py mongo-to-solr HRC_20220929 e472d26a-b343-4547-ac7d-cccfc5e890a7
```

## TODOS:

- [ ] TODO: Describe dataloading once it is repaired
- [ ] stream video from S3 and don't add it as an environment variable
