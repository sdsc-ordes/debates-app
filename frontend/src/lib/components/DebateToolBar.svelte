<script lang="ts">
    import FileDownload from "./FileDownload.svelte";
    import type { SignedUrl } from "$lib/interfaces/metadata.interface";

    export let downloadUrls: SignedUrl[] = [];
</script>

<div class="toolbar">
    <div><FileDownload {downloadUrls} /></div>
</div>

<style>
    .toolbar {
        background-color:var(--on-primary);
        width: 100%;
        height: 2rem;
        border-radius: 2rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding: 5px;
        margin: 0;
        box-sizing: border-box;
    }
</style>
