import requests
import hashlib
import hmac
import datetime
import base64
from typing import Optional
import argparse
import os
import json
import glob


class BloodhoundClient:
    def __init__(self, token_key: str, token_id: str, endpoint: str):
        self._token_key = token_key
        self._token_id = token_id
        self._endpoint = endpoint

    def format_url(self, uri: str) -> str:
        return f"{self._endpoint}{uri}"

    def request(
        self, method: str, uri: str, body: Optional[bytes] = None
    ) -> requests.Response:

        digester = hmac.new(self._token_key.encode(), None, hashlib.sha256)

        digester.update(f"{method}{uri}".encode())

        digester = hmac.new(digester.digest(), None, hashlib.sha256)

        datetime_formatted = datetime.datetime.now().astimezone().isoformat("T")

        digester.update(datetime_formatted[:13].encode())

        digester = hmac.new(digester.digest(), None, hashlib.sha256)

        if body is not None:
            digester.update(body)

        return requests.request(
            method=method,
            url=self.format_url(uri),
            headers={
                "User-Agent": "bhe-python-sdk 0001",
                "Authorization": f"bhesignature {self._token_id}",
                "RequestDate": datetime_formatted,
                "Signature": base64.b64encode(digester.digest()),
                "Content-Type": "application/json",
            },
            data=body,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-k", "--token-key", help="Bloodhound api token key", required=True
    )

    parser.add_argument(
        "-i", "--token-id", help="Bloodhound api token id", required=True
    )

    parser.add_argument(
        "-e",
        "--endpoint",
        help="Bloodhound endpoint",
        default="http://localhost:8080",
    )

    args = parser.parse_args()

    client = BloodhoundClient(
        args.token_key,
        args.token_id,
        args.endpoint,
    )

    files = glob.glob("output/*.json")

    for file in files:
        print("Creating bloodhound file-upload job...")

        try:
            with open(file, "r") as f:
                data = json.load(f)
        except:
            print(f"Malformed JSON detected for file: {file} ...skipping")
            continue

        response = client.request("POST", "/api/v2/file-upload/start")

        if response.status_code != 201:
            print(response.status_code)
            print(response.content)
            raise Exception("Received non-OK response when making API request")

        upload_job_id = response.json()["data"]["id"]

        print("Uploading data set to bloodhound...")

        response = client.request(
            "POST",
            f"/api/v2/file-upload/{upload_job_id}",
            json.dumps(data).encode("utf-8"),
        )

        if response.status_code != 202:
            print(response.status_code)
            print(response.content)
            raise Exception("Received non-OK response when making API request")

        os.remove(file)

        print("Data set successfully uploaded to bloodhound")

    print("Done")
