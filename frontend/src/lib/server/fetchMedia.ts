import type { S3Key, SignedUrls } from "$lib/interfaces/metadata.interface";
import { BackendUrl } from "$lib/config";

export async function fetchMedia(
    s3Prefix: string,
    objectKeys: string[],
    mediaKey: string,
): Promise<SignedUrls> {
    try {
        // FastAPI endpoint to retrieve signed URLs
        const apiUrl = `${BackendUrl}/get-media-urls`;

        // Request payload for signed URLs
        const payload = JSON.stringify({
            prefix: s3Prefix,
            objectKeys: objectKeys,
            mediaKey: mediaKey,
        });

        // Fetch signed URL from FastAPI backend
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: payload,
        });
        if (!response.ok) {
            throw new Error(`Error fetching signed URL: ${response.statusText}`);
        }

        // Extract JSON from the response
        const data = await response.json();
        const signedUrls = data;
        return signedUrls;
    } catch (error) {
        console.error('Error in fetchMedia:', error);
        throw error;
    }
}
