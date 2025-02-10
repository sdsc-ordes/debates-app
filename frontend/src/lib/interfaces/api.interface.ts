import type { Subtitle, SubtitleType, Speaker } from "$lib/interfaces/metadata.interface";

export interface DownloadRequest {
    prefix: string;
    key: string;
}

export interface SpeakerUpdateRequest {
    prefix: string;
    speakers: Speaker[]
}

export interface SubtitleUpdateRequest {
    prefix: string,
    segmentNr: number,
    subtitles: Subtitle[],
    subtitleType: SubtitleType
}
