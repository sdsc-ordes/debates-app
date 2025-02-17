## Architecture

The architecture consists of 3 parts:

- [**processing pipeline**](processing.md): for the video and audio files to derive transcripts translations and additional metadata

```mermaid
flowchart LR
    A[Media: Video/Audio] --Processing--> B(Transcript/Translation)
    C[Additional Sources] --Webscraping--> D(Additional Metadata)
    B --> E[(Objectstore S3)]
    D --> E
```

- [**loading results into secondary databases**](loading.md): the processed data is loaded into structured databases to improve findability

```mermaid
flowchart LR
  S[(Object Store S3)] --load--> E{SRT Parser}
  E --metadata--> B[(Structured Metadata MongoDB)]
  E --segments--> C[(Search Engine Solr)]
```

- [**serving and enriching metadata via a WebUI**](webui.md): the Webui allows to search in the debates and to annotate and correct the speaker statements

```mermaid
flowchart LR
    subgraph Backend[Debates Backend]
        M{Debates API}
        C[(Search Engine Solr)]
        S[(Object Store S3)]
        B[(Structured Metadata MongoDB)]
    end
    subgraph UI[Debates GUI]
        F(GUI Searchpage)
        E(GUI Videoplayer)
    end
    M -- serve --> F
    M -- serve --> E
    C -- load --> M
    B -- load --> M
    S -- signed urls --> M
    E -- correct --> M
    style UI fill:white
    style Backend fill:white
```
