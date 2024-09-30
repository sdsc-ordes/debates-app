# Political Debates UI

## Setup docker compose

User Interface for political debates with Solr and Sveltekit

```
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

Check that Solr is up and that the core `debates` was created.

## Load the data

### Process the data


### Load the data into Solr

Make sure the data is expected in the directory `data/solr` that is mounted 
by the docker compose into `debates_solr/data` on the solr docker container


Load data on demand:

```
docker-compose exec solr post -c debates /debates_solr/data
```

In case you want to reload data in Solr (which needed on a schema change): 

- Delete data: Go to the Solr Ui: go to documents and enter as xml:

```
<delete><query>*:*</query></delete>
```

Afterwards load the data again as described above.

### Frontend development

Once the Solr and proxy are up in the docker compose, the Frontend can als be developed locally: see https://github.com/sdsc-ordes/debates-ui.git
