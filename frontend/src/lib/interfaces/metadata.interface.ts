export interface ResponseMetadata {
    success: boolean;
    data: DebateMetadata;
}

export interface DebateMetadata {
    _id: string;
    s3_prefix: string;
    version_id: string;
    original: boolean;
    created_at: string;
    debate: Debate;
    media_key: string;
    s3_keys: S3Key[];
    format: string;
    speakers: Speaker[];
    segments: Segment[];
    subtitles: Subtitle[];
    subtitles_en: Subtitle[];
}

export interface Debate {
    schedule: string;
    type: string;
    tags: string[];
    public: boolean;
}

export interface S3Key {
    key: string;
    type: string;
    description: string;
}

export interface Speaker {
    speaker_id: string;
    name: string;
    role_tag: string;
}

export interface Segment {
    speaker_id: string;
    start: number;
    end: number;
    segment_nr: number;
}

export interface Subtitle {
    index: number;
    start: number;
    end: number;
    content: string[];
    segment_nr: number;
}

export interface SignedUrl {
    label: string;
    url: string;
}

export interface SignedUrls {
    signedUrls: SignedUrl[];
    signedMediaUrl: string;
}

export enum SubtitleTypeEnum {
    Transcript = "Transcript",
    Translation = "Translation",
}

export interface SubtitleType {
    type: SubtitleTypeEnum;
}
