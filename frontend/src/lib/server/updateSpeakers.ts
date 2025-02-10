import { BackendUrl } from "$lib/config";
import type { Speaker } from "$lib/interfaces/metadata.interface";

export async function updateSpeakers(prefix: string, speakers: Speaker[]) {
    try {
        // FastAPI endpoint to update speakers
        const apiUrl = `${BackendUrl}/update-speakers`;
        // Request payload for update speakers
        const payload = JSON.stringify({
            prefix: prefix,
            speakers: speakers,
        });

        // Update speakers on FastApi Backend
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: payload,
        });
        if (!response.ok) {
            throw new Error(`Error saving speakers: ${response.statusText}`);
        };
    } catch (error) {
        console.error('Error in saving speakers:', error);
        throw error;
    }
}
