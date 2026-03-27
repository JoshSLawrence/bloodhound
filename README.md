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

### Corporate Environment / Custom CA Certificates

If you're in a corporate environment where a firewall is intercepting and
resigning SSL/TLS requests, you'll need to add your custom CA certificate(s)
to the Docker image:

1. Place your certificate file(s) (`.crt` format) in the repository directory
2. Edit the `Dockerfile` and uncomment the certificate lines (around line 17-20):

   ```dockerfile
   # COPY <certfile> /usr/local/share/ca-certificates/
   # RUN update-ca-certificates
   ```

3. Replace `<certfile>` with your certificate filename(s). For multiple certificates:

   ```dockerfile
   COPY cert1.crt cert2.crt /usr/local/share/ca-certificates/
   RUN update-ca-certificates
   ```

4. Rebuild the image and recreate the container:

   ```bash
   docker compose up -d --build azurehound
   ```

   This will rebuild the image with your certificates and recreate the container.

## Getting Started

1. Clone this repo
2. Copy the example environment file and configure it:

   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your Azure/Entra credentials:

   - `AZURE_CLIENT_ID`
   - `AZURE_CLIENT_SECRET`
   - `AZURE_TENANT_ID`

4. Execute `docker compose up -d` to start the Bloodhound services (app-db,
   graph-db, and bloodhound - azurehound will fail that is OK)

5. Access the bloodhound instance at `http://localhost:8080/ui/login`

6. Login as `admin`, the default password can be found in `bloodhound.config.json`

7. Create a new user (optional) and generate an API key and ID, see:
   [Create a non-personal API key/ID pair](https://bloodhound.specterops.io/integrations/bloodhound-api/working-with-api#create-a-non-personal-api-key%2Fid-pair).

8. Add/Update the following environment variables to your `.env` file:

   - `BLOODHOUND_TOKEN_KEY` (the API key you generated)
   - `BLOODHOUND_TOKEN_ID` (the API ID you generated)

9. Execute `docker compose up -d --force-recreate azurehound`

10. The `azurehound` container will automatically run and:

    - Collect data from the target Entra and Azure environment
    - Generate an `output.json` file with the collected data
    - Upload the data to the Bloodhound instance via the API
    - Exit after completion (this is expected behavior)

> [!TIP]
> You can start the `azurehound` container to refetch data from Entra and Azure
> on demand

## Refreshing the database

While using your instance, you may wish to update your data set in the underlying
neo4j database.

### Updating with new data

To refresh the data with current information from Azure/Entra:

1. Execute `docker compose up azurehound` to re-run the azurehound container
2. The container will collect fresh data and upload it to Bloodhound

> [!IMPORTANT]
> This will add to the existing data set rather than replacing it. This can result
> in duplicate data - you way wish to instead wipe the data and refresh it. See
> the next section.

### Wiping the database

To completely wipe the neo4j database and start fresh:

#### Option 1: Stop only the graph database and remove its volume

```bash
docker compose stop graph-db
docker volume rm bloodhound_neo4j-data
docker compose up -d graph-db
```

#### Option 2: Take down everything with volumes (nuclear option)

```bash
docker compose down --volumes
docker compose up -d
```

After wiping the database, run the azurehound container to populate it with
fresh data:

```bash
docker compose up azurehound
```

> [!TIP]
> Option 1 is recommended as it only affects the neo4j database, keeping your
> Bloodhound configuration and postgres data intact. Option 2 will reset everything
> including user accounts and settings.
