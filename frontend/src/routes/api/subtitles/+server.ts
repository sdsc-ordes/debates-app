import type { SubtitleUpdateRequest } from "$lib/interfaces/api.interface";
import { updateSubtitles } from '$lib/server/updateSubtitles';

export async function POST({ request }) {
    try {
        const subtitleUpdateRequest: SubtitleUpdateRequest = await request.json();
        await updateSubtitles(
            subtitleUpdateRequest.prefix,
            subtitleUpdateRequest.segmentNr,
            subtitleUpdateRequest.subtitles,
            subtitleUpdateRequest.subtitleType,
        );
        // 204 No Content is a typical success response for a
        // PUT/PATCH/POST when there's no body to return
        return new Response(null, { status: 204 });

    } catch (error) {
        console.error("API Speaker Update Error:", error);
        return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }
}