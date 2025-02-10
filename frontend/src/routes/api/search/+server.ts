import type { SolrQuery } from "$lib/interfaces/search.interface";
import { searchSolr } from "$lib/server/search";

export async function POST({ request }) {
    try {
        const solrQuery: SolrQuery = await request.json();
        const searchResults = await searchSolr(solrQuery);
        return new Response(JSON.stringify({ raw_response: searchResults }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (error) {
        console.error("API Error:", error);
        return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
}
