<script lang="ts">
    import { goto } from '$app/navigation';
    import { replaceWithHighlightedVersion } from '$lib/utils/highlightSearchTerms';
    import type { SolrDocument, SolrHighlighting } from "$lib/interfaces/search.interface";
    import {
        formatTimeForDisplay,
        displayIsoDate,
    } from "$lib/utils/displayUtils";

    export let highlighting: SolrHighlighting;
    export let doc: SolrDocument;

    const navigateToVideoPlayer = () => {
        goto(`/${encodeURIComponent(doc.s3_prefix)}?start=${encodeURIComponent(doc.start)}`);
    };
</script>

<div class="statement">
    <!-- <hr /> -->
    <div
        class="card"
        on:click={() => navigateToVideoPlayer(doc.s3_prefix)}
        role="button"
        tabindex="0"
        on:keydown={(e) =>
            (e.key === "Enter" || e.key === " ") &&
            navigateToVideoPlayer(doc.s3_prefix)}
    >
        <div class="card-body">
            <div class="card-title-large">{doc.debate_type} {doc.debate_session}</div>
            <p class="card-body-large truncated">
                {#if highlighting}
                    {@html replaceWithHighlightedVersion(
                        doc.statement,
                        highlighting?.[doc.id]?.statement,
                    ).join(" ")}
                {:else}
                    {doc.statement.join(" ")}
                {/if}
            </p>
            <div class="datetime-container">
                <div class="date-time-item">
                    <i class="fa fa-calendar" aria-hidden="true"></i>
                    <small class="card-subtle"
                        >{displayIsoDate(doc.debate_schedule)}</small
                    >
                </div>
                <div class="date-time-item">
                    <i class="fa fa-clock" aria-hidden="true"></i>
                    <small class="card-subtle"
                        >{formatTimeForDisplay(doc.start)} - {formatTimeForDisplay(
                            doc.end,
                        )}</small
                    >
                </div>
                <small class="card-subtle">{doc.statement_type}
                    {#if doc.statement_language}
                        ({doc.statement_language})
                    {/if}</small
                >
            </div>
        </div>
    </div>
</div>

<style>
    .datetime-container {
        display: flex;
        gap: 1rem;
        align-items: center;
    }

    .card-body-large.truncated {
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .card:hover {
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    }

    .date-time-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .fa {
        font-size: 1rem;
        color: grey;
    }

</style>
