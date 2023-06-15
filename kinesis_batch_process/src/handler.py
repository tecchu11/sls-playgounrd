import asyncio

import aiohttp
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.batch import (
    AsyncBatchProcessor,
    EventType,
    async_process_partial_response,
)
from aws_lambda_powertools.utilities.batch.types import PartialItemFailureResponse
from aws_lambda_powertools.utilities.data_classes.kinesis_stream_event import (
    KinesisStreamRecord,
)

async_processor = AsyncBatchProcessor(
    event_type=EventType.KinesisDataStreams,
)
logger = Logger()
session_timeout = aiohttp.ClientTimeout(total=3)


async def record_handler(record: KinesisStreamRecord) -> int:
    code: int = record.kinesis.data_as_json()["status"]
    httpbin = f"https://httpbin.org/status/{code}"
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        try:
            async with session.get(url=httpbin) as response:
                res = await response.text()
                st = response.status
                if response.status == 200:
                    logger.info("Success")
                elif response.status == 400:
                    logger.error("Validation Error")
                else:
                    raise RuntimeError("Response was failure status")
        except RuntimeError as err:
            logger.exception(f"Got failure response status code {st} and body {res}")
            raise RuntimeError("failed") from err
        except asyncio.TimeoutError as timeout_error:
            logger.exception(f"Timeout to call httpbin When calling with {code}")
            raise RuntimeError(
                "Failed to call httpbin because of timeout",
            ) from timeout_error
        except Exception as unhandled:
            logger.exception("Unhandled exception was raised")
            raise RuntimeError("failed") from unhandled

    return response.status


@logger.inject_lambda_context(log_event=False)
def handler(event, context) -> PartialItemFailureResponse:
    """
    npx sls invoke local -f kinesis-batch-process -s local -p tests/event.json
    :param event: Kinesis stream
    :param context: Lambda context
    :return: For reporting failure items to kinesis
    """
    return async_process_partial_response(
        event=event,
        record_handler=record_handler,
        processor=async_processor,
        context=context,
    )
