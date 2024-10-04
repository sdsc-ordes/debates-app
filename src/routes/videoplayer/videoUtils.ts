
import { parseSRT } from './parseSrt';
import { updateSubtitle } from './subtilteUtils';

export async function loadSubtitles(startTime: number, video: HTMLVideoElement) {
    const response = await fetch('/input/subtitles.srt');
    const srtText = await response.text();
    const parsedData = parseSRT(srtText);
    video.currentTime = startTime;
    onTimeUpdate(video, parsedData.parsedSubtitles);
    video.play();
    return parsedData;
}

export function onTimeUpdate(video: HTMLVideoElement, subtitles: any[]) {
    console.log("on time update");
    console.log(video.currentTime);
    console.log(subtitles)
    const updatedData = updateSubtitle(video.currentTime, subtitles);
    return {
        subtitle: updatedData.subtitle,
        currentSpeaker: updatedData.currentSpeaker,
    };
}

export function jumpToTime(video: HTMLVideoElement, time: number) {
    video.currentTime = time;
    video.play(); // Optionally start playing after jump
}
