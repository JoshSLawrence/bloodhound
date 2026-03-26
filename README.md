# Bloodhound

This repo is an implementation of the Docker compose deployment method
for Bloodhound provided by [SpectreOps](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart).

## Requirements

- An Entra app registration, with the following permissions:
  - Microsoft Graph: `Directory.Read.All`
  - Entra: `Directory Reader` or `Global Reader`
  - Azure: `Reader` (On all Subscriptions you wish to audit, or more
    easily the Root Management Group)
- You will need to set the following environment variables in a `.env` file
    in this repo:
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_TENANT_ID`
  - `BLOODHOUND_TOKEN_KEY` (after initial setup, see below)
  - `BLOODHOUND_TOKEN_ID` (after initial setup, see below)
- Docker or Docker Desktop

## Getting Started

1. Clone this repo
2. Set up your `.env` file with the required environment variables:
   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_TENANT_ID`
3. Execute `docker compose up -d` to start the Bloodhound services (app-db,
    graph-db, and bloodhound)
4. Access the bloodhound instance at `http://localhost:8080/ui/login`
5. Login as `admin`, the default password can be found in `bloodhound.config.json`
6. Create a new user (optional) and generate an API key and ID, see:
    [Create a non-personal API key/ID pair](https://bloodhound.specterops.io/integrations/bloodhound-api/working-with-api#create-a-non-personal-api-key%2Fid-pair).
7. Add the following environment variables to your `.env` file:
   - `BLOODHOUND_TOKEN_KEY` (the API key you generated)
   - `BLOODHOUND_TOKEN_ID` (the API ID you generated)
8. Execute `docker compose up -d --force-recreate
9. The `azurehound` container will automatically run and:
   - Collect data from the target Entra and Azure environment
   - Generate an `output.json` file with the collected data
   - Upload the data to the Bloodhound instance via the API
   - Exit after completion (this is expected behavior)

> [!NOTE]
> You can start the `azurehound` container to refetch data from Entra and Azure
> on demand

## Refreshing the database

While using your instance, you may wish to update your data set in the underlying
neo4j database.

### Updating with new data

To refresh the data with current information from Azure/Entra:

1. Execute `docker compose up azurehound` to re-run the azurehound container
2. The container will collect fresh data and upload it to Bloodhound

> [!Note]
> This will add to the existing data set rather than replacing it. This can result
> in duplicate data - you way wish to instead wipe the data and refresh it.

### Wiping the database

To completely wipe the database and start fresh, delete the neo4j volume:

1. Execute `docker compose down`
2. List the volumes via `docker volume ls`
3. Identify the neo4j volume (should be named `bloodhound_neo4j-data`)
4. Remove the volume by executing `docker volume rm bloodhound_neo4j-data`
5. Execute `docker compose up -d` to spin up the containers

Docker will recreate the neo4j volume, and the `azurehound` container will fetch
fresh data from your Entra and Azure environments and upload it to your Bloodhound
instance, which will then write the data into the fresh neo4j database.
