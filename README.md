# Political Debates UI

User Interface for political debates with Solr and Sveltekit

Load data on demand:

```
docker run --rm -v "$PWD/data/solr:/debates_solr/data" --network=host solr post -c debates /debates_solr/data
```