#!/bin/bash

cd "$(dirname "$0")"

if [ -f "output.json" ]; then
    rm "output.json"
fi

./azurehound list \
    -a $AZURE_CLIENT_ID \
    -s $AZURE_CLIENT_SECRET \
    -t $AZURE_TENANT_ID  \
    -o "output.json"

source .venv/bin/activate

python3 ./ingestdata.py -k $BLOODHOUND_TOKEN_KEY -i $BLOODHOUND_TOKEN_ID -e $BLOODHOUND_ENDPOINT
