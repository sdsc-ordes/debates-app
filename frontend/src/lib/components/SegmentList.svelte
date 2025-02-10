<script lang="ts">
  import type {
    TimeUpdateParameters,
  } from "$lib/interfaces/mediaplayer.interface";
  import type {
    Segment,
    Speaker,
  } from "$lib/interfaces/metadata.interface";
  import { formatTimeForDisplay } from "$lib/utils/displayUtils";
  import { jumpToTime } from "$lib/utils/mediaStartUtils";
  import { displaySpeaker } from "$lib/utils/displayUtils";

  export let segments: Segment[] = [];
  export let speakers: Speaker[] = [];
  export let timeUpdateParameters: TimeUpdateParameters;
  export let mediaElement: HTMLVideoElement;
</script>

<div class="scrollable-container">
  <ol>
    {#each segments as segment}
      <li>
        <div
          class="card text-center {segment.segment_nr ===
          timeUpdateParameters.displaySegmentNr
            ? 'current'
            : 'other'}"
          on:click={() => jumpToTime(mediaElement, segment.start)}
          role="button"
          tabindex="0"
          on:keydown={(e) =>
            (e.key === "Enter" || e.key === " ") &&
            jumpToTime(mediaElement, segment.start)}
          id='segment-{ segment.segment_nr }'
        >
          <div class="card-body">
            <div class="card-title-small" style="color=inherit;">
              {@html displaySpeaker(segment.speaker_id, speakers)}
            </div>
            <div class="date-time-item">
              <i
                class="fa fa-clock {segment.segment_nr ===
                timeUpdateParameters.displaySegmentNr
                  ? 'current'
                  : 'other'}"
                aria-hidden="true"
              ></i>
              <small
                class="card-subtle {segment.segment_nr ===
                timeUpdateParameters.displaySegmentNr
                  ? 'current'
                  : 'other'}"
                >{formatTimeForDisplay(segment.start)} - {formatTimeForDisplay(
                  segment.end,
                )}</small
              >
            </div>
          </div>
        </div>
      </li>
    {/each}
  </ol>
</div>

<style>
  .scrollable-container {
    overflow-y: auto;
    max-width: 100%;
  }
  ol li {
    list-style-type: none;
  }

  .card {
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    margin-bottom: 1rem;
  }
  .card-body {
    display: flex;
    flex-direction:row;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
  }

  /* Styles for the current speaker card */
  .card.current {
    color: var(--on-primary);
    background-color: var(--primary-dark-color);
  }

  .fa {
    font-size: 1rem;
    color: var(--primary-dark-color);
  }
  .fa.current {
    color: var(--on-primary);
  }

  .card-subtle {
    color: var(--primary-dark-color);
  }
  .card-subtle.current {
    color: var(--on-primary);
  }

</style>
