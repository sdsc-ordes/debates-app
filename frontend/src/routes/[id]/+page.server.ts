import type { PageServerLoad } from "./$types";
import type { SignedUrls, ResponseMetadata } from "$lib/interfaces/metadata.interface";
import { fetchMedia } from "$lib/server/fetchMedia";
import { fetchMetadata } from "$lib/server/fetchMetadata";

export const load: PageServerLoad = async ({ params }) => {
    try {
        const s3Prefix: string = params.id;
        const metadata: Promise<ResponseMetadata> = await fetchMetadata(s3Prefix);
        const objectKeys: string[] = metadata.debate.s3_keys.map(item => item.name);
        const mediaKey = metadata.debate.media.key;
        const signedUrls: SignedUrls = await fetchMedia(
            s3Prefix,
            objectKeys,
            mediaKey,
        );
        return {
            prefix: s3Prefix,
            media: metadata.debate.media,
            debate: metadata.debate,
            speakers: metadata.speakers.speakers,
            segments: metadata.segments.segments,
            subtitles: metadata.subtitles.subtitles,
            subtitles_en: metadata.subtitles_en.subtitles,
            signedUrls: signedUrls,
        };
    } catch (error) {
        console.error("Error loading collections:", error);
        return {
            video: null,
            error: "Could not load video data",
        };
    }
};
