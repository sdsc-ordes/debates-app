export function jumpToTime(mediaElement: HTMLMediaElement, start: number) {
    mediaElement.currentTime = start;
    mediaElement.play();
}
