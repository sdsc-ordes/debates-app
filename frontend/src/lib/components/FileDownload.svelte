<script lang="ts">
    import type { SignedUrl } from "$lib/interfaces/backend.interface";

    export let downloadUrls: SignedUrl[] = [];

    let selectedFileUrl = downloadUrls[0]?.url;

    $: signedUrl = selectedFileUrl || null;

    function handleDownload() {
        if (signedUrl) {
            const link = document.createElement("a");
            link.href = signedUrl;
            link.setAttribute("download", getFilenameFromUrl(signedUrl));
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }

    function getFilenameFromUrl(url: string): string {
        // Extract the filename from the URL
        const parts = url.split("/");
        return parts[parts.length - 1] || "download";
    }
</script>

<!-- UI Layout -->
<div class="download">
    <!-- <span>Select and Download a File</span> -->

    <form class="toolbar-form" on:submit|preventDefault>
        <!-- Dropdown for file selection -->
        <select class="toolbar-select" bind:value={selectedFileUrl}>
            <option value="" disabled>Select a file</option>
            {#each downloadUrls as file}
                <option value={file.url}>{file.label}</option>
            {/each}
        </select>
    </form>

    <button
        class="secondary-button"
        type="button"
        on:click={handleDownload}
        disabled={!signedUrl}
    >
        Download
    </button>
</div>

<style>
    .download {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .toolbar-form {
        margin: 0;
    }

    .toolbar-select {
        height: 20px; /* Matches toolbar height */
        font-size: 12px;
        border: 1px solid var(--primary-color);
        border-radius: 10px;
        padding: 0 10px;
        color: var(--text-color);
        background-color: var(--on-primary);
        cursor: pointer;
        transition: background-color 0.3s, color 0.3s;
    }


</style>
