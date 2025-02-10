<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import type { SolrQuery } from "$lib/interfaces/search.interface";

    export let solrQuery: SolrQuery;

    const dispatch = createEventDispatcher();

    function submitForm() {
        dispatch("submit");
    }

    function resetForm() {
        solrQuery.queryTerm = "";
        dispatch("reset");`~`
    }
</script>

<div>
    <form on:submit|preventDefault={submitForm} class="search-form">
        <input
            class="search-input"
            type="text"
            bind:value={solrQuery.queryTerm}
            placeholder="Enter search term"
        />
        <button class="option-button" type="button" on:click={resetForm}>
            <i class="fa fa-xmark"></i>
        </button>
        <button class="button-primary" type="submit">
            <i class="fa fa-search"></i> Search
        </button>
    </form>
</div>

<style>
    .search-form {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        width: 100%;
        max-width: 40rem;
        margin: 0 auto;
        padding: 10px;
        padding-right: 20px;
        border-radius: 50px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        /* background-color: var(--background-color); */
    }
    .search-input {
        flex: 1;
        padding: 10px 15px;
        border: none;
        border-radius: 50px;
        font-size: 12px;
        color: var(--text-color);
        outline: none;
        transition: border-color 0.3s ease;
    }

    .option-button {
        /* margin-top: 0.5rem;
        font-size: 0.9rem; */
        color: gray;
        background: none;
        border: none;
        cursor: pointer;
        text-align: left;
        /* margin-left: 2rem; */
    }
</style>
