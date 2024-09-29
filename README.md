# Political Debates UI

User Interface for political debates with Solr and Sveltekit

```
docker-compose build --no-cache
docker-compose up -d --force-recreate
```

Load data on demand:

```
docker-compose exec solr post -c debates /debates_solr/data
```

Delete all data: go to documents and enter as xml:

```
<delete><query>*:*</query></delete>
```

# TODO

1. change field types in solr for time_start and time_end  -> pint
2. transform the times in pyvideo
3. load data again
4. transform dates to isodates


