<script lang="ts">
  import { onMount } from "svelte";
  import { onMediaTimeUpdate } from "$lib/utils/mediaTimeUpdate";
  import { jumpToTime } from "$lib/utils/mediaStartUtils";
  import type { TimeUpdateParameters } from "$lib/interfaces/mediaplayer.interface";
  import type {
    Subtitle,
    Speaker,
    Segment,
  } from "$lib/interfaces/metadata.interface";
  export let startTime: number;
  export let timeUpdateParameters: TimeUpdateParameters;
  export let subtitles: Subtitle[] = [];
  export let subtitles_en: Subtitle[] = [];
  export let speakers: Speaker[] = [];
  export let segments: Segment[] = [];
  export let mediaElement: HTMLMediaElement;
  export let mediaUrl: string;
  export let media;

  function handleTimeUpdate() {
    timeUpdateParameters = onMediaTimeUpdate(
      mediaElement.currentTime,
      subtitles,
      subtitles_en,
      segments,
    );
  }

  onMount(async () => {
    if (startTime) {
      jumpToTime(mediaElement, startTime);
    }
  });
</script>

<div class="media-container">
  {#if media.type === "video"}
    <!-- svelte-ignore a11y-media-has-caption -->
    <video
      class="media"
      bind:this={mediaElement}
      on:timeupdate={handleTimeUpdate}
      controls
      disablePictureInPicture
    >
      <source src={mediaUrl} type="{media.type}/{media.format}" />
      Your browser does not support the video tag.
    </video>
  {:else if media.type === "audio"}
    <audio
      class="media"
      bind:this={mediaElement}
      on:timeupdate={handleTimeUpdate}
      controls
      autoplay
    >
      <source src={mediaUrl} type="{media.type}/{media.format}" />
      Your browser does not support the audio tag.
    </audio>
  {/if}
</div>

<style>
  .media {
    max-width: 100%;
    object-fit: contain;
  }

  .media-container {
    width: 100%;
    height: 100%; /* Forces it to respect the parent container */
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
</style>
