# Solr Instance for Political Debates

Build docker images

```
docker build -t my-solr .
```

Then precreate core with custom config

```
docker run -p 8983:8983 my-solr solr-precreate debates /opt/solr/server/solr/configsets/debates
````

## How Solr was customized

The repos was build by running first the standard Solr image:

```
docker run -d -p 8983:8983 --name my_solr solr solr-precreate debates
``` 

After that the config was copied out: 

```
docker cp my_container:/opt/solr/server/solr/configsets/mycore /mysolr/config
```

## Customization of the Solr

The Config can now be customized in the local directory. If it is customized in Solr, the directory needs to be fetched from Docker again as described above
to persist the changes

## Load data

The Solr is part of a bigger project where data loading is described:
https://github.com/sdsc-ordes/political-debates-ui
