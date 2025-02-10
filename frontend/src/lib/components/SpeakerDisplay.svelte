<script lang="ts">
  import type { TimeUpdateParameters } from "$lib/interfaces/mediaplayer.interface";
  import type { Speaker } from "$lib/interfaces/metadata.interface";
  import { canEdit } from "$lib/stores/auth";
  let errorMessage: string | null = null;

  export let speakers: Speaker[] = [];
  export let timeUpdateParameters: TimeUpdateParameters;
  export let s3Prefix: string;
  let editSpeakers = false;

  function toggleEditSpeakers() {
    editSpeakers = !editSpeakers;
  }

  async function saveSpeakers() {
    const SpeakerUpdateRequest = {
      prefix: s3Prefix,
      speakers: speakers,
    }
    editSpeakers = !editSpeakers;
    errorMessage = null;
    try {
      const response = await fetch('/api/speakers', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(SpeakerUpdateRequest)
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

<div class="card">
  <div class="card-body">
    {#each speakers as speaker}
      {#if speaker.speaker_id === timeUpdateParameters.displaySpeakerId && speaker}
        <div class="card-title-small">{speaker.speaker_id}</div>

        <!-- EDITABLE SECTION -->
        {#if $canEdit}
          <p class="card-subtle">Edit speaker details below:</p>

          {#if editSpeakers}
            <form class="speaker-form">
              <label for="speaker-name" class="input-label">Name</label>
              <input
                id="speaker-name"
                placeholder="Enter name"
                type="text"
                bind:value={speaker.name}
                class="editable-input"
              />
              <label for="speaker-tags" class="input-label">Role</label>
              <input
                id="speaker-tags"
                placeholder="Enter role"
                type="text"
                bind:value={speaker.role_tag}
                class="editable-input"
              />
            </form>
          {:else}
            <!-- DISPLAY MODE -->
            <div class="speaker-display">
              <label class="input-label">Name</label>
              <div class="display-text">{speaker.name || "Name not provided"}</div>

              <label class="input-label">Role</label>
              <div class="display-text">{speaker.role_tag || "Role not provided"}</div>
            </div>
          {/if}
        {:else}
          <!-- NON-EDITABLE VIEW -->
          <div class="speaker-display">
            <label class="input-label">Name</label>
            <div class="display-text">{speaker.name || "Name not provided"}</div>

            <label class="input-label">Role</label>
            <div class="display-text">{speaker.role_tag || "Role not provided"}</div>
          </div>
        {/if}

        <!-- BUTTON CONTROLS -->
        {#if $canEdit}
          <div class="button-group">
            {#if editSpeakers}
              <button class="secondary-button" on:click={toggleEditSpeakers} aria-label="Cancel">
                Cancel
              </button>
              <button class="secondary-button" on:click={saveSpeakers} aria-label="Save">
                Save
              </button>
            {:else}
              <button class="secondary-button" on:click={toggleEditSpeakers} aria-label="Edit">
                Edit
              </button>
            {/if}
          </div>
        {/if}
      {/if}
    {/each}
  </div>
</div>


<style>
  .card {
    /* width: fit-content; */
    max-width: 100%;
    max-height: 100%;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    padding: 1rem;
    box-sizing: border-box;
  }

  .card-body {
    display: flex;
    flex-direction: column;
    /* gap: 1rem; */
  }

  .speaker-form,
  .speaker-display {
    display: flex;
    flex-direction: column;
    /* gap: 1rem; */
  }

  .input-label {
    font-size: 14px;
    font-weight: 500;
    color: #333;
  }

  .editable-input {
    height: 40px;
    padding: 0 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    width: 100%;
  }

  .editable-input:focus {
    border-color: var(--primary-color);
    outline: none;
  }

  .editable-input::placeholder {
    color: gray;
    font-style: italic;
  }
  .display-text {
    height: 40px;
    padding: 0 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
    color: grey;
    display: flex;
    align-items: center;
  }

  .button-group {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 1rem;
  }

</style>
