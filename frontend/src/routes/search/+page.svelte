<script lang="ts">
  import SearchForm from "$lib/components/SearchForm.svelte";
  import FacetCounts from "$lib/components/FacetCounts.svelte";
  import SearchResultContainer from "$lib/components/SearchResultContainer.svelte";
  import type {
    SolrHighlighting, SolrQuery, SolrResponse, SolrFacetCounts,
    SolrDocument
  } from '$lib/interfaces/search.interface';
  import { createDefaultSolrQuery } from "$lib/interfaces/search.interface";
  import { onMount } from "svelte";

  let solrQuery: SolrQuery = createDefaultSolrQuery();
  let solrResponse: SolrResponse;
  let highlighting: SolrHighlighting;
  let docs: SolrDocument[];
  let facetCounts: SolrFacetCounts;
  let errorMessage: string | null = null; // For displaying errors

  async function handleSearch() {
    errorMessage = null; // Clear any previous errors
    try {
      const response = await fetch('/api/search', {  // Call the API endpoint
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(solrQuery) // Send the solrQuery in the body
      });

      if (!response.ok) {
        const errorData = await response.json(); // Try to get error details
        errorMessage = errorData.error || `Search failed: ${response.status} ${response.statusText}`; // Display detailed error
        console.error(errorMessage);
        return; // Stop processing if the request failed
      }

      const data = await response.json();
      solrResponse = data.raw_response;
      highlighting = solrResponse?.highlighting ?? null;
      facetCounts = solrResponse?.facet_counts ?? null;
      docs = solrResponse?.response?.docs ?? [];
    } catch (error) {
      errorMessage = `An unexpected error occurred: ${error.message}`;
      console.error(errorMessage);
    }
  }

  function handleReset() {
    solrQuery = createDefaultSolrQuery()
    handleSearch();
  }
  onMount(() => {
    handleReset();
  });
</script>

<svelte:head>
  <title>Political Debates Search</title>
  <meta name="description" content="Political Debates Search" />
</svelte:head>

<div class="container">
  <div class="row">
    <div class="col-md-4">
      <SearchForm {solrQuery}
        on:submit={handleSearch}
        on:reset={handleReset}
      />
      {#if facetCounts}
      <FacetCounts
        {solrQuery}
        onSearch={handleSearch}
        {facetCounts}
      />
      {/if}
    </div>
    {#if solrResponse}
      <div class="col-md-8">
        <SearchResultContainer
          {docs}
          {highlighting}
        />
      </div>
    {/if}
  </div>
</div>
