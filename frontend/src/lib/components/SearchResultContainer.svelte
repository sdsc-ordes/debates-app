<script lang="ts">
  import SearchResultItem from "$lib/components/SearchResultItem.svelte";
  import type { SolrDocument, SolrHighlighting } from "$lib/interfaces/search.interface";

  export let docs: SolrDocument[];
  export let highlighting: SolrHighlighting;

</script>

<div class="container">
  <div class="statements">
    {#if docs && docs.length > 0}
      {#each docs as doc}
        <SearchResultItem {doc} {highlighting} />
      {/each}
    {:else}
      <p>No statements available.</p>
    {/if}
  </div>
</div>

<style>
  .statements {
      display: flex;
      flex-direction: column;
      gap: 1rem;
  }
</style>
