import json

import boto3
from mypy_boto3_kinesis.client import KinesisClient

kinesis_client: KinesisClient = boto3.client(
    service_name="kinesis",
    region_name="ap-northeast-1",
    endpoint_url="http://localhost:4566",
)


def make_datas() -> list[[int, bytes]]:
    def data(i: int) -> dict:
        return {
            "status": i,
        }

    return [[i, json.dumps(data(i)).encode("utf-8")] for i in [200, 400, 500, 503]]


if __name__ == "__main__":
    records = [
        {
            "Data": b,
            "PartitionKey": str(a),
        }
        for [a, b] in make_datas()
    ]
    put_response = kinesis_client.put_records(
        Records=records,
        StreamARN="arn:aws:kinesis:ap-northeast-1:000000000000:stream/foo-stream",
    )
