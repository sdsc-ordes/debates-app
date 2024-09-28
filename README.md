# Solr Instance for Political Debates

Build docker images

```
docker build -t my-solr .
```

Then precreate core with custom config

```
docker run -p 8983:8983 my-solr solr-precreate debates /opt/solr/server/solr/configsets/debates
````
