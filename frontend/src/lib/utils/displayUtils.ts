import type { Speaker } from "$lib/interfaces/metadata.interface";

export function formatTimeForDisplay(seconds: number): string {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    const hrsStr = String(hrs).padStart(1, "0");
    const minsStr = String(mins).padStart(2, "0");
    const secsStr = String(secs).padStart(2, "0");
    if (hrs) {
        return `${hrsStr}:${minsStr}:${secsStr}`;
    }
    return `${minsStr}:${secsStr}`;
}

export function displayIsoDate(isoDate: string): string {
    const date = new Date(isoDate);
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based, so add 1
    const day = date.getDate().toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${month}/${day}/${year}`;
}

export function displaySpeaker(speakerId: string, speakers: Speaker[]): string {
    const speaker = speakers.find(speak => speak.speaker_id === speakerId);
    if (!speaker) {
        throw new Error(`Speaker with ID ${speakerId} not found.`);
    }
    return speaker.name || speaker.speaker_id;
}
