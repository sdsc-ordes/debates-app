# Roadmap

## Debates Processing Pipeline

- **UN Media DataLoader**: `odtp-unog-digitalrecordings-downloader`: Component to download a recording from the UNOG Digital Recordinfs platform.
- **Match Faces to Speakers**: `odtp-faces-identifier`: Component to identify faces from video frames.
- **S3 Dataloader** `odtp-s3datauploader`: Component to upload data output to an S3 folder

## Debates App Features

- **Authentication and Authorization**: add a proper authentication and authorization provider

## Debates Dataloader

- **Backend API**: improve the [API documentation](../architecture/api.md): add response structure for api routes

## Additional Configuration

- [**S3 File Structure**](../architecture/processing.md) The file names in the S3 are currently hard coded: they can be made configurable
