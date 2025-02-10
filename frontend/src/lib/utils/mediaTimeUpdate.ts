import type {
    TimeUpdateParameters,
} from "$lib/interfaces/mediaplayer.interface";
import type {
    Subtitle, Speaker, Segment
} from "$lib/interfaces/metadata.interface";

export function onMediaTimeUpdate(
    currentTime: number,
    subtitles: Subtitle[],
    subtitles_en: Subtitle[],
    segments: Segment[],
): TimeUpdateParameters {
    const displaySegmentNr = getDisplaySegmentNr(currentTime, segments);
    const displaySubtitleIndex = getDisplaySubtitleIndex(currentTime, subtitles);
    const displaySubtitleEnIndex = getDisplaySubtitleIndex(currentTime, subtitles_en);
    const displaySpeakerId = getDisplaySpeakerId(displaySegmentNr, segments);
    return {
        displaySubtitleIndex,
        displaySubtitleEnIndex,
        displaySegmentNr,
        displaySpeakerId,
    }
}

function getDisplaySegmentNr(
    currentTime: number,
    segments: Segment[],
) {
   let currentSegment = segments.find(seg => currentTime >= seg.start && currentTime <= seg.end);
   if (currentSegment) {
       return currentSegment.segment_nr;
   }
   let previousSegment = segments.reduce((maxSeg, seg) => {
        if (currentTime >= seg.end && (!maxSeg || seg.end > maxSeg.end)) {
            return seg;
        }
        return maxSeg;
    }, null);
    if (previousSegment) {
        return previousSegment.segment_nr;
    }
    return -1;
}

function getDisplaySubtitleIndex(
    currentTime: number,
    subtitles: Subtitle[],
) {
   let currentSubtitle = subtitles.find(sub => currentTime >= sub.start && currentTime <= sub.end);
   if (currentSubtitle) {
       return currentSubtitle.index;
   }
   let previousSubtitle = subtitles.reduce((maxSub, sub) => {
        if (currentTime >= sub.end && (!maxSub || sub.end > maxSub.end)) {
            return sub;
        }
        return maxSub;
    }, null);
    if (previousSubtitle) {
        return previousSubtitle.segment_nr;
    }
    return -1;
}

function getDisplaySpeakerId(
    displaySegmentNr: number,
    segments: Segment[],
) {
    if (displaySegmentNr) {
        let segment = segments.find(seg => seg.segment_nr === displaySegmentNr);
        if (segment) {
            return segment.speaker_id
        }
    }
    return -1
}