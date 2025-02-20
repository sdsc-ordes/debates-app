# Dataloader

## Overview

!!! note

    Loading the data into the App assumes that you have the backend running:
    See [Install options](../install/index.md) for setup options

The processed data is loaded from **Pipeline S3** into 3 databases:

- **App S3**: S3 Database for processed data: this is done manually with only a small modification see below
- **App MongoDB** Mongo database for all metadata on speakers, segments, transcripts and translations
- **App Solr** Solr search engine where speaker segments are loaded as documents into Solr

``` mermaid
flowchart LR
    subgraph WebApp[Web Application]
        B[(App S3)]
        E{SRT Parser}
        C[(App MongoDB)]
        D[(App Solr)]
    end
    A[(Pipeline S3)] -- manual --> B
    B --> E
    E --> C
    E --> D
    style WebApp fill:white
```

## Loading into the App S3

All [files are from Pipeline S3](processing.md/#outputs-in-s3) loaded into App S3: this is currently done manually.
App S3 needs just one extra file `HRC_20220328T0000-metadata.yml`: it is derived from `HRC_20220328T0000-files.yml`.

```hl_lines="4"
debates
└── HRC_20220328T0000
    ├── HRC_20220328T0000-files.yml
    ├── HRC_20220328T0000-metadata.yml
    ...
```

Example for `HRC_20220328T0000-metadata.yml`:

```hl_lines="7-30"
s3_prefix: HRC_20160622T0000
media:
  key: HRC_20160622T0000.mp4
  type: video
  format: mp4
s3_keys:
  - name: HRC_20220328T0000.json
    type: json
    description: JSON file containing metadata transcription ...
  - name: HRC_20220328T0000-files.yml
    type: yml
    description: YAML file containing metadata of the files ...
  - name: HRC_20220328T0000.mp4
    type: mp4
    description: MP4 video file from the 2020 03 28 00:00 session
  - name: HRC_20220328T0000-original.wav
    type: wav
    description: Original audio file from the 2020 03 28 00:00 session
  - name: HRC_20220328T0000-transcription_original.srt
    type: srt
    description: Transcription file in SRT format ...
  - name: HRC_20220328T0000-transcription_original.pdf
    type: pdf
    description: PDF file containing the transcription ...
  - name: HRC_20220328T0000-translation_original_english.srt
    type: srt
    description: Translation file in SRT format to English ...
  - name: HRC_20220328T0000-translation_original_english.pdf
    type: pdf
    description: PDF file containing the English translation ...
context:
  type: "Human Rights Council"
  session: "32th session"
  public: True
schedule:
  date: "2016-06-22"
  time: "10:00"
  timezone: "Europe/Zurich"
```

- The metadata in `context` and  `schedule` have been derived from https://conf.unog.ch/digitalrecordings/en
- `s3_prefix`: is the prefix or directory on S3, where the files for the media item are stored
- `media`: points to the actual media file that is played in the `media player`:

`media` subkeys:

   - `key`: is the actual media file
   - `type`: can be `video`or `audio`
   - `format`: format is the media file format: for videos `mp4` is supported and for audio files `wav`.

## Loading into Mongodb and Solr

!!! warning

    Only do these steps on a fresh set up when you database is empty: otherwise it will mess up your existing data

Once the environment is setup, the commands to load data into the mongodb and Solr are the following per media item:

Then load the data from App S3:

```
python debates.py s3-to-mongo-solr HRC_20220328T0000
```

## Start API Server

After this step the data should be available. You can now start the backend:

```
python debates.py serve
```

You will find the api documentation at `http://localhost:8000/docs` or as json file at `http://localhost:8000/openapi.json`
For your convenience it has also been added to this documentation: [api documentation](api.md)
