# Bloodhound

This repo is an implementation of the Docker compose deployment method
for Bloodhound provided by [SpectreOps](https://bloodhound.specterops.io/get-started/quickstart/community-edition-quickstart).

## Requirements

- An Entra app registration, with the following permissions:
  - Microsoft Graph: Directory.Read.All
  - Entra: Directory Reader
  - Azure: Reader (On all Subscriptions, or more easily the Root Management Group)
- You will need to set the following environment variables in your system,
    or set them in a `.env` file in this repo:
  - AZURE_CLIENT_ID
  - AZURE_CLIENT_SECRET
  - AZURE_TENANT_ID
- Docker or Docker Desktop

## Getting Started

1. Clone this repo
2. Execute `docker compose up -d`
3. Access the bloodhound instance at `http://localhost:8080/ui/login`
4. Login as `admin`, the default password can be found in `bloodhound.config.json`
5. Create a new user and generate an api key and id, see:
    [Create a non-personal API key/ID pair](https://bloodhound.specterops.io/integrations/bloodhound-api/working-with-api#create-a-non-personal-api-key%2Fid-pair).
6. Update the Docker compose azurehound service with your api key and id:

_Note: if you have not already, setup your .env file
    as outlined in the [Requirements](#requirements) section_

```yml
  azurehound:
    build: .
    environment:
      - AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
      - AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}
      - AZURE_TENANT_ID=${AZURE_TENANT_ID}
      - BLOODHOUND_TOKEN_KEY=<YOUR TOKEN KEY HERE>
      - BLOODHOUND_TOKEN_ID=<YOUR TOKEN ID HERE>
      - BLOODHOUND_ENDPOINT=http://bh-docker-win-bloodhound-1:8080
    ```

7. Execute `docker compose down` and then `docker compose up -d`
8. After a minute or so, the `azurehound` container should exit having uploaded
    data pulled using azurehound to your bloodhound instance.

## Refreshing the database

While using your instance, you may wish to update you data set in the uderlying
neo4j database.

While you could re-run the `azurehound` container, it will just add to data that
is already present.

To wipe the database, the easiest way is to delete the neo4j volume defined by docker.

1. Execute `docker compose down`
2. List the volumes via `docker volume ls`
3. Identity the neo4j volume, it should be named `bh-docker-win_neo4j-data`
4. Remove the volume by executing `docker volume rm bh-docker-win_neo4j-data`
  - Swap out "bh-docker-win_neo4j-data" in the command for your name as needed
5. Execute `docker compose up -d` to spin up the containers

Docker will recreate the neo4j volume, and shortly after the `azurehound` container
will finish fetching data from your Entra and Azure environments. It will post the
data to your bloodhound instnace which will then write your data into the fresh
neo4j database.
