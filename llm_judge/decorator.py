import time
import uuid
from datetime import datetime
from functools import wraps


def llm_metrics(func):
    """
    Measures metrics for the Judge LLM.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        request_id = str(uuid.uuid4())

        start_time = datetime.now()
        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)

            end = time.perf_counter()
            end_time = datetime.now()

            latency = round(end - start, 3)

            return {
                "request_id": request_id,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "latency": latency,
                "status": "success",
                **result
            }

        except Exception as e:

            end = time.perf_counter()
            end_time = datetime.now()

            latency = round(end - start, 3)

            return {
                "request_id": request_id,
                "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                "latency": latency,
                "status": "failed",
                "error": str(e)
            }

    return wrapper


def agent_metrics(func):
    """
    Measures metrics for the LLM response being evaluated.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        try:
            result = func(*args, **kwargs)

            end = time.perf_counter()

            latency = round(end - start, 3)

            return {
                "agent_name": result["agent_name"],
                "prompt": result["prompt"],
                "response": result["response"],
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"],
                "latency": latency,
                "model": result["model"]
            }

        except Exception as e:

            end = time.perf_counter()

            latency = round(end - start, 3)

            return {
                "agent_name": kwargs.get("agent_name", "unknown"),
                "prompt": kwargs.get("prompt", ""),
                "response": "",
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "latency": latency,
                "model": "unknown",
                "error": str(e)
            }

    return wrapper