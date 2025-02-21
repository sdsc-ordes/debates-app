# Debates App

## About

This app allows to load and correct transcripts for media such as video or audio.

The transcript that the app was made for where AI derived: the AI provides both:

- transcript
- translation

both are expected as SRT file divided by speakers such as:

```
1
00:00:00,031 --> 00:00:17,811
[SPEAKER_06]:  Pasamos inmediatamente al tema 9, ...
```

The inputs are assumed in an S3: currently they need to be uploaded manually

The `dataloader` component:

- puts these videos in a Mongodb
- adds the statements per speaker and debate in a Solr search engine
- serves as a backend to connect to these two databases

The `frontend` component:

- has a search page to search in the speakers statements
- offers a media player page to compare transcript and translation with the media and annotate or correct

## Setup

The app is setup via docker-compose. See documentation for the details.
