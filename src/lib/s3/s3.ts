import type { MediaSources } from "$lib/interfaces/videoplayer.interface";

export function getMediaSources(s3Prefix: string): MediaSources {
  let mediaSources: MediaSources;
  if (s3Prefix === 'HRC_20220328') {
    mediaSources = {
      videoSrc: "/input/HRC_20220328.mp4",
      trackSrc: "/input/HRC_20220328.srt",
    }
  }
  if (s3Prefix === 'HRC_20220929') {
    mediaSources = {
      videoSrc: "/input/HRC_20220929.mp4",
      trackSrc: "/input/HRC_20220929.srt",
    }
  }
  return mediaSources;
}