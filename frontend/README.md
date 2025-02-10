# political debates ui: frontend

## About

This is the frontend for https://github.com/sdsc-ordes/political-debates-ui.
The frontend is made in SvelteKit. It has two pages:
- A search page to search in video transcripts on a Solr Instance
- A videoplayer page where a video can be played along with transcript and speaker information that can be edited. The metadata of the video is retrieved form a mongo db.
- There is an edit route: `/edit`: going on that route allows to switch into edit mode and edit the video metadata and spreaker information


## Technology

- The frontend uses SvelteKit.

Dependencies:
- The transcript and video are expected in SRT: currently there is just one video with transcript provided and the video and SRT file are stored in `static/input/video.mp4` and  `static/input/subtitles.srt`. These two files are just part of the videoplayer itself. #TODO: move these files to an S3 instance.
- The frontend needs access to a Solr instance up with the search metadata for the videos, see setup section
- It also needs a mongodb instance to get the editable metadata from.

## Setup

Because of the complicated setup, it is recommended to use a docker compose that is provided in the main repository: https://github.com/sdsc-ordes/political-debates-ui, see setup instructions there.
There is a `env.dist` file provided to show the environment variables that it needs. In case the dependencies are all accessible it can be setup on its own with the following commands:

```
npm install
pnpm dev
```
