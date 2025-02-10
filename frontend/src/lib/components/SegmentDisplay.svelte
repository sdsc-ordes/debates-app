<script lang="ts">
  import type { TimeUpdateParameters } from "$lib/interfaces/mediaplayer.interface";
  import { type Subtitle, SubtitleTypeEnum } from "$lib/interfaces/metadata.interface";
  import { canEdit } from "$lib/stores/auth";
  import { jumpToTime } from "$lib/utils/mediaStartUtils";

  export let subtitles: Subtitle[] = [];
  export let subtitles_en: Subtitle[] = [];
  export let timeUpdateParameters: TimeUpdateParameters;
  export let mediaElement: HTMLVideoElement;
  export let s3Prefix: string;

  let editSubtitlesTranscription: boolean = false;
  let editSubtitlesTranslation: boolean = false;

  let errorMessage: string | null = null; // For displaying errors

  const transcript = SubtitleTypeEnum.Transcript;
  const translation = SubtitleTypeEnum.Translation;

  function updateSubtitle(index: number, updatedText: string) {
    subtitles[index].content = updatedText;
  }

  function toggleEditSubtitlesTranscription() {
    editSubtitlesTranscription = !editSubtitlesTranscription;
  }
  function toggleEditSubtitlesTranslation() {
    editSubtitlesTranslation = !editSubtitlesTranslation;
  }

  function saveSubtitle$Transcription(): void {
    updateSubtitles(s3Prefix, timeUpdateParameters.displaySegmentNr, subtitles, transcript)
    editSubtitlesTranscription = !editSubtitlesTranscription;
  }
  function saveSubtitle$Translation(): void {
    updateSubtitles(s3Prefix, timeUpdateParameters.displaySegmentNr, subtitles_en, translation)
    editSubtitlesTranslation = !editSubtitlesTranslation;
  }
  async function updateSubtitles(prefix: string, segmentNr: number, subtitles: Subtitle[], type: string) {
    const subtitleUpdateRequest = {
      prefix: prefix,
      segmentNr: segmentNr,
      subtitles: subtitles,
      subtitleType: type,
    }
    errorMessage = null;
    try {
      const response = await fetch('/api/subtitles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(subtitleUpdateRequest)
      });

      if (!response.ok) {
        const errorData = await response.json();
        errorMessage = errorData.error || `Search failed: ${response.status} ${response.statusText}`; // Display detailed error
        console.error(errorMessage);
        return;
      }
    } catch (error) {
      errorMessage = `An unexpected error occurred: ${error.message}`;
      console.error(errorMessage);
    }
  }
</script>

<div class="side-by-side">
  <div class="text-block">
    <div
      style="display: flex;
    align-items: center;
    justify-content: start;
    gap: 1rem;
    width: 90%;"
    >
      <div class="card-title-small">Transcription</div>
      {#if $canEdit && !editSubtitlesTranscription}
        <button
          class="secondary-button"
          on:click={toggleEditSubtitlesTranscription}
          aria-label="Edit"
          >Edit
        </button>
      {:else if editSubtitlesTranscription}
        <button
          class="secondary-button"
          on:click={toggleEditSubtitlesTranscription}
          aria-label="Cancel"
          >Cancel
        </button>
        <button
          class="secondary-button"
          on:click={() => saveSubtitle$Transcription()}
          aria-label="Save"
        >
          Save
        </button>
      {/if}
    </div>
    <p>
      {#each subtitles as subtitle, index}
        {#if subtitle.segment_nr === timeUpdateParameters.displaySegmentNr}
          <span
            class={index === timeUpdateParameters.displaySubtitleIndex - 1
              ? "highlighted"
              : ""}
            on:click={() => jumpToTime(mediaElement, subtitle.start)}
          >
            {#if editSubtitlesTranscription}
              <div>
                <textarea
                  id={`subtitle-${index}`}
                  bind:value={subtitle.content}
                  on:input={(e) => updateSubtitle(index, e.target.value)}
                  class={`editable-textarea ${
                    index === timeUpdateParameters.displaySubtitleIndex - 1 ? "highlighted-textarea" : ""
                  }`}
                />
              </div>
            {:else}
              {subtitle.content}
            {/if}
          </span>
        {/if}
      {/each}
    </p>
  </div>
  <div class="text-block">
    <div
      style="display: flex;
    align-items: center;
    justify-content: start;
    gap: 1rem;
    width: 100%;"
    >
      <div class="card-title-small">Translation</div>
      {#if $canEdit && !editSubtitlesTranslation}
        <button
          class="secondary-button"
          on:click={toggleEditSubtitlesTranslation}
          aria-label="Edit"
          >Edit
        </button>
      {:else if editSubtitlesTranslation}
        <button
          class="secondary-button"
          on:click={toggleEditSubtitlesTranslation}
          aria-label="Cancel"
          >Cancel
        </button>
        <button
          class="secondary-button"
          on:click={() => saveSubtitle$Translation()}
          aria-label="Save"
        >
          Save
        </button>
      {/if}
    </div>
    <p>
      {#each subtitles_en as subtitle, index}
        {#if subtitle.segment_nr === timeUpdateParameters.displaySegmentNr}
          <span
            class={index === timeUpdateParameters.displaySubtitleEnIndex - 1
              ? "highlighted"
              : ""}
            on:click={() => jumpToTime(mediaElement, subtitle.start)}
          >
            {#if editSubtitlesTranslation}
              <div>
                <textarea
                  id={`subtitle-${index}`}
                  bind:value={subtitle.content}
                  on:input={(e) => updateSubtitle(index, e.target.value)}
                  class={`editable-textarea ${
                    index === timeUpdateParameters.displaySubtitleEnIndex - 1 ? "highlighted-textarea" : ""
                  }`}
                />
              </div>
            {:else}
              {subtitle.content}
            {/if}
          </span>
        {/if}
      {/each}
    </p>
  </div>
</div>

<style>
  .side-by-side {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    max-height: 300px;
    padding: 0.5rem;
  }

  .text-block {
    flex: 1;
    display: flex;
    flex-direction: column;
  }

  .text-block p {
    overflow-y: auto;
  }

  .highlighted {
    color: var(--secondary-color);
  }

  .editable-textarea {
    width: 100%;
    height: 50px;
  }

  .highlighted-textarea {
    border: 2px solid var(--secondary-color);
  }

  p {
    margin: 0;
    padding: 0;
    word-wrap: break-word;
  }

</style>
