<script lang="ts">
  import type { SolrQuery, SolrFacetCounts } from "$lib/interfaces/search.interface";
  import { displayIsoDate } from "$lib/utils/displayUtils";

  export let solrQuery: SolrQuery;
  export let facetCounts: SolrFacetCounts;
  export let onSearch: (solrQuery: SolrQuery) => void;

  const displayFunctions: { [key: string]: (label: string) => string } = {
    debate_schedule: (label) => displayIsoDate(label),
  };

  // Default display function if no specific function is found for a facet field
  const defaultDisplayFunction = (label: string) => label;

  function getDisplayFunction(fieldKey: string): (label: string) => string {
    return displayFunctions[fieldKey] || defaultDisplayFunction;
  }

  // Helper function to get facet values as key-value pairs
  const getFacetFields = (
    facetFields: Record<string, Array<string | number>>,
  ) => {
    let fields = [];
    for (const [key, values] of Object.entries(facetFields)) {
      let facets = [];
      for (let i = 0; i < values.length; i += 2) {
        facets.push({ label: values[i], count: values[i + 1] });
      }
      fields.push({ key, facets });
    }
    return fields;
  };

  function handleFacetAddClick(facetField: string, facetValue: string) {
    if (!solrQuery.facetFieldValues) {
            solrQuery.facetFieldValues = [];
    }
    solrQuery.facetFieldValues.push({ facetField: facetField, facetValue: facetValue });
    onSearch(solrQuery);
  }

  function handleFacetRemoveClick(facetField: string, facetValue: string) {
    if (!solrQuery.facetFieldValues) return;

    // Filter out the facet that matches both field and value
    solrQuery.facetFieldValues = solrQuery.facetFieldValues.filter(
        (facet) => !(facet.facetField === facetField && facet.facetValue === facetValue)
    );

      onSearch(solrQuery);
  }

  function isActive(facetField: string, facetLabel: string): boolean {
    return solrQuery.facetFieldValues?.some(
        (facet) => facet.facetField === facetField && facet.facetValue === facetLabel
    ) ?? false;
  }
</script>

{#if facetCounts}
  <div class="filters">
    {#each getFacetFields(facetCounts.facet_fields) as field}
      <h4 class="facet-title">
        {field.key.replace(/_/g, " ")}
      </h4>
      <div class="facets">
        {#each field.facets as facet}
          {#if facet.count && facet.label}
            <div class="facet-row">
              <button
                class="facet-item {isActive(field.key, facet.label)
                  ? 'active'
                  : ''}"
                on:click={() => handleFacetAddClick(field.key, facet.label)}
                on:click={() => handleFacetAddClick(field.key, facet.label)}
              >
                {getDisplayFunction(field.key)(facet.label)}
              </button>
              <small class="card-subtle">{facet.count}</small>
              {#if isActive(field.key, facet.label)}
                <button
                  class="option-button"
                  type="button"
                  on:click={() => handleFacetRemoveClick(field.key, facet.label)}
                >
                  <i class="fa fa-xmark" style="color:var(--primary-dark-color)"></i>
                </button>
              {/if}
            </div>
          {/if}
        {/each}
      </div>
    {/each}
  </div>
{:else}
  <p>No facet counts available.</p>
{/if}

<style>
  .filters {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 12px;
  }

  .facets {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding-left: 1rem;
  }

  .facet-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .facet-title {
    font-family: var(--body-font);
    font-size: 16px;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    text-transform: lowercase;
    color: var(--primary-color);
  }

  .facet-item {
    color: var(--primary-color);
    border: none;
    padding: 5px 10px;
    border-radius: 10px;
    cursor: pointer;
    transition: background-color 0.3s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
  }

  .facet-item.active {
    background-color: var(--primary-color);
    color: var(--on-primary);
  }
</style>
