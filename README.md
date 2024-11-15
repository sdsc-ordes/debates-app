# debates-dataloader

Dataloader for videos transcriptions

## Install

The package management is done with [rye](https://rye.astral.sh/)

```
git clone git@github.com:sdsc-ordes/debates-dataloader.git
cd debates-dataloader
rye install
rye sync
source .venv/bin/activate
```

## Environment Variables

```
# External Service settings:
# must match the docker compose settings for the services
SOLR_URL=http://localhost:8010/solr/debates/
MONGO_DB=debates
MONGO_VIDEO_COLLECTION=videos
S3_BUCKET_NAME=debates
S3_ACCESS_KEY=[your-S3-access-key]
S3_SECRET_KEY=[your-S3-secret-key]

# Use this for local
API_HOST="127.0.0.1"
MONGO_URL=mongodb://localhost:27017/
S3_SERVER=http://localhost:9000
FRONTEND_SERVER=http://localhost:5173

# Use this for compose
API_HOST="0.0.0.0"

# this is for the PROD S3
PROD_S3_BUCKET_NAME=[your-prod-S3-bucket-name]
PROD_S3_ACCESS_KEY=[your-prod-S3-access-key]
PROD_S3_SECRET_KEY=[your-prod-S3-secret-key]
PROD_S3_REGION_NAME=[your-prod-S3-region-name]
```

## Use

The dataloader includes the following parts:

- cli commands to manage S3, Solr and MongoDB
- fastapi route to serve media urls from S3


### Start Fast API Server

```
python src/debates.py serve
```

### CLI Commands

```
python src/debates.py --help
```
