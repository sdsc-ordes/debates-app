import type { SpeakerUpdateRequest } from "$lib/interfaces/api.interface";
import { updateSpeakers } from '$lib/server/updateSpeakers';

export async function POST({ request }) {
    try {
        const speakerUpdateRequest: SpeakerUpdateRequest = await request.json();
        await updateSpeakers(speakerUpdateRequest.prefix, speakerUpdateRequest.speakers);
        // 204 No Content is a typical success response for a
        // PUT/PATCH/POST when there's no body to return
        return new Response(null, { status: 204 });

    } catch (error) {
        console.error("API Speaker Update Error:", error);
        return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
}
