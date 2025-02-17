# Server setup

The setup on a server is similar to the compose setup. It will not described in detail here.

## Environment Variables

The env variables are similar to the [compose setup](compose.md): you have to set:

- [environment for the debates app](compose.md#environment-variables-for-debates-app)
- [environment for the frontend](compose.md#environment-variables-for-frontend)

## Docker compose

The server setup has it's own docker compose file `docker-compose.yml`. The docker compose commands will use that file, but you can also specify it with `-f docker-compose.yml`

```
docker compose build
docker compose up -d
```

## Proxy Server

Their is an additional reverse proxy that has the following tasks:

- password protect access to the debates app for all users
- restrict access to the route `edit` to the `editor user`
- provide lets encrypt certification to make the debates api available under `https`

## Load data

See [compose setup](compose.md#load-data)
