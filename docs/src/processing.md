# Processing Pipeline

The processing pipeline ...

``` mermaid
graph TB
    ExternalUNDatabase[(External UN Database)] --> UNScrapper[ODTP UN Scrapper]
    subgraph ODTP
    direction TB
        UNScrapper --> ODTPPyannoteWhisper[ODTP Pyannote Whisper]
        ODTPPyannoteWhisper --> ODTPTranslation[ODTP Translation]
        ODTPTranslation
    end
    ODTPTranslation --> UNS3[(Pipeline S3)]
```

Existing components:

- **ODTP UN Scrapper** [`odtp-unog-digitalrecordings-scrapper`](https://github.com/sdsc-ordes/odtp-unog-digitalrecordings-scrapper). Component to scrap and download metadata from the UNOG Digital Recordings platform.
- **ODTP Pyannote Whisper** [`odtp-pyannote-whisper`](https://github.com/sdsc-ordes/odtp-pyannote-whisper). Component to diarize and transcribe audios and videos
- **ODTP Translation**: [`odtp-trascription2pdf`](https://github.com/sdsc-ordes/odtp-transcriptions2pdf). Component to generate pdfs from a transcription json file.

Not yet developped:

- **UN Media DataLoader**: `odtp-unog-digitalrecordings-downloader`: Component to download a recording from the UNOG Digital Recordinfs platform.
- **Match Faces to Speakers**: `odtp-faces-indentifier`: Component to identify faces from video frames.
- **S3 Dataloader** `odtp-s3datauploader`: Component to upload data output to an S3 folder

## Outputs in S3

The S3 of the Pipeline contains the results for each media file processing: the results are structured in the following way:

```hl_lines="1 2 3 7 10 12"
debates
└── HRC_20220328T0000
    ├── HRC_20220328T0000-files.yml
    ├── HRC_20220328T0000-original.wav
    ├── HRC_20220328T0000-transcription_original.json
    ├── HRC_20220328T0000-transcription_original.pdf
    ├── HRC_20220328T0000-transcription_original.srt
    ├── HRC_20220328T0000-translation_original_english.json
    ├── HRC_20220328T0000-translation_original_english.pdf
    ├── HRC_20220328T0000-translation_original_english.srt
    ├── HRC_20220328T0000.json
    └── HRC_20220328T0000.mp4
```

The operational important outputs are highlighted above and described below:

- `debates`: is the S3 bucket for all outputs
- `HRC_20220328T10000.mp4`: is the original media file that was processed: a prefix is derived from the name `HRC_20220328T10000`. All outputs belonging to the media file are stored under that prefix in the S3
- `HRC_20220328T0000-files.yml`: contains all files with descriptions
- `HRC_20220328T0000-transcription_original.srt`: the SRT file with the transcription
- `HRC_20220328T0000-translation_original_english.srt` the SRT file with the translation
- `HRC_20220328T0000.mp4`: the media file that is played in the AppUI videoplayer

### SRT files

SRT is a commonly known Standard for subtitles. Below your see an example of an SRT file. The SRT files that the pipeline  outputs already contain speaker information in form of a speaker IDs such as `SPEAKER_06`. The speaker_ids are derived
by diarization.

```
1
00:00:00,031 --> 00:00:17,811
[SPEAKER_06]:  Pasamos inmediatamente al tema 9, ...

2
00:00:17,811 --> 00:00:31,451
[SPEAKER_06]:  Procedemos ahora a la presentación ...

3
00:00:31,451 --> 00:00:47,751
[SPEAKER_06]:  Tengo el placer de dar la bienvenida ...

4
00:00:47,811 --> 00:00:50,631
[SPEAKER_06]:  Excelencia, querida embajadora, tiene la palabra.

5
00:00:55,145 --> 00:00:57,305
[SPEAKER_00]:  Thank you, Chair Passon.

6
00:00:57,305 --> 00:01:00,525
[SPEAKER_00]:  Excellencies, ladies and gentlemen,

```

## Additonal outputs

Example of `HRC_20220328T0000-files.yml`

```
files:
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
```

After the media has been processed it is loaded into the Debates App via the [dataloader](dataloader.md).
