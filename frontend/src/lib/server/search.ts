import { BackendUrl } from "$lib/config";
import type { SolrQuery } from "$lib/interfaces/search.interface";

export async function searchSolr(solrQuery: SolrQuery) {
    try {
        // FastAPI endpoint to fetch metadata
        const apiUrl = `${BackendUrl}/search-solr`;
        const facetFields: string[] = [
            "debate_schedule", "statement_type", "debate_session", "speaker_name", "speaker_role_tag"];
        const payload = JSON.stringify({
            queryTerm: solrQuery.queryTerm,
            sortBy: solrQuery.sortBy,
            facetFields: facetFields,
            facetFilters: solrQuery.facetFieldValues,
        });

        // Fetch metadata from FastAPI backend
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: payload,
        });

        if (!response.ok) {
            throw new Error(`Error fetching metadata: ${response.statusText}`);
        }

        // Extract JSON from the response
        const data = await response.json();
        return data.raw_response;
    } catch (error) {
        console.error('Error in searchSolr:', error);
        throw error;
    }
}