import type { DebateMetadata } from "$lib/interfaces/metadata.interface";
import { BackendUrl } from "$lib/config";

export async function fetchMetadata(s3Prefix: string): DebateMetadata {
    try {
        // FastAPI endpoint to fetch metadata
        const apiUrl = `${BackendUrl}/mongo-metadata`;

        // Request payload for fetching metadata
        const payload = JSON.stringify({ prefix: s3Prefix, expiration: 3600 });

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
        const metaData = data;
        return metaData;
    } catch (error) {
        console.error('Error in fetchMetadata:', error);
        throw error;
    }
}
