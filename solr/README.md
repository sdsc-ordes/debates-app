# political debates ui: Solr

## About

This is the Solr setup for https://github.com/sdsc-ordes/political-debates-ui.
It provides the custom schema for the video transcript data. 

## Schema

The video transcripts are stored as segments of the video. Each segments consists of one speaker and all the subtitles that belongs to his `statement`, before it is another speakers turn.

Example Document: not all fields are mentioned in this example:

```
    {
        "start": 0.006,
        "end": 50.071,
        "speaker_name": "SPEAKER_06",
        "statement": [
            "We will immediately move on to topic 9, open statement, topic 9 of the agenda, entitled Racism, Racial Discrimination, Xenophobia and Connected Forms of Intolerance, Follow-up and Application of the Declaration and Action Program of Durban.",
            "We now proceed to the presentation of the report of the Working Group",
            "Intergovernmental on the effective application of the Durban Action Program on its nineteenth session.",
            "I have the pleasure of welcoming Your Excellency Mrs. Marie Chantal Ruacallina, permanent representative of Rwanda, to the United Nations Office in Geneva, and President and Rapporteur of the Working Group for the presentation of the report.",
            "Your Excellency, dear Ambassador, you have the floor."
        ],
        "segment_id": 1,
    }
```

The schema started with Solr provided managed schema.

### How Solr schema started

The repos was build by running first the standard Solr image and then copying out the schema from `/opt/solr/server/solr/configsets/debates` with `docker cp`: see setup section on how to run the docker container.

### How Solr schema is customized

All fields in the documents that need search functionality should be added to the Solr schema: for changing the schema there are two options:

- the schema can be changed directly on `schema/managed-schema.xml
- mount Solr with Docker as described in the set up section. Then add the field on the Solr UI and copy the field from `/opt/solr/server/solr/configsets/debates

## Setup

The Solr instance can be setup on its own by a docker image:

```
docker build -t my-solr .
```

Then precreate core with custom config

```
docker run -p 8983:8983 my-solr solr-precreate debates /opt/solr/server/solr/configsets/debates
```

## Load Documents

The data is loaded by https://github.com/sdsc-ordes/debates-dataloader
