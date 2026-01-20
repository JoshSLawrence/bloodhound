#!/bin/bash

cd "$(dirname "$0")"

if [ -f "output/azurehound.json" ]; then
    rm "output/azurehound.json"
fi

echo "id $AZUREHOUND_CLIENT_ID"
echo "secret $AZUREHOUND_CLIENT_SECRET"
echo "tenant $AZUREHOUND_TENANT_ID"

./azurehound list \
    -a $AZURE_CLIENT_ID \
    -s $AZURE_CLIENT_SECRET \
    -t $AZURE_TENANT_ID  \
    -o "output/azurehound.json"

source .venv/bin/activate

python3 ./ingestdata.py -k $BLOODHOUND_TOKEN_KEY -i $BLOODHOUND_TOKEN_ID -e $BLOODHOUND_ENDPOINT
