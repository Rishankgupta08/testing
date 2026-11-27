import time
import logging
from typing import Callable, Any, Tuple, Optional

import requests

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def api_call_with_timeout_handling(
    func: Callable[..., Any],
    *args,
    retries: int = 3,
    backoff_factor: float = 0.5,
    timeout: Optional[Tuple[float, float]] = None,
    **kwargs,
) -> Any:
    """
    Executes an API call function with built‑in timeout handling and optional retries.

    Parameters
    ----------
    func : Callable[..., Any]
        The function that performs the API request. It should accept a ``timeout`` keyword
        argument compatible with ``requests`` (e.g., a float or a ``(connect, read)`` tuple).
    *args : tuple
        Positional arguments passed to ``func``.
    retries : int, optional
        Number of retry attempts after a timeout occurs. Default is ``3``.
    backoff_factor : float, optional
        Factor for exponential back‑off between retries. Sleep time is calculated as
        ``backoff_factor * (2 ** attempt)`` seconds. Default is ``0.5``.
    timeout : tuple or float, optional
        Timeout value forwarded to ``func``. If ``None``, the function is called without
        a timeout argument.
    **kwargs : dict
        Keyword arguments passed to ``func``.

    Returns
    -------
    Any
        The result returned by ``func`` if successful.

    Raises
    ------
    requests.exceptions.Timeout
        Propagated if all retry attempts fail.
    Exception
        Any other exception raised by ``func`` is re‑raised immediately.
    """
    attempt = 0
    while True:
        try:
            if timeout is not None:
                kwargs["timeout"] = timeout
            return func(*args, **kwargs)
        except requests.exceptions.Timeout as exc:
            attempt += 1
            if attempt > retries:
                logger.error(
                    "API request timed out after %d attempts: %s", attempt - 1, exc
                )
                raise
            sleep_time = backoff_factor * (2 ** (attempt - 1))
            logger.warning(
                "Timeout occurred (attempt %d/%d). Retrying in %.2f seconds...",
                attempt,
                retries,
                sleep_time,
            )
            time.sleep(sleep_time)
        except Exception:
            # Propagate any non‑timeout exceptions immediately
            raise

# Example usage (remove or comment out in production)
if __name__ == "__main__":
    def fetch_example(url: str, **kw) -> requests.Response:
        return requests.get(url, **kw)

    try:
        response = api_call_with_timeout_handling(
            fetch_example,
            "https://httpbin.org/delay/3",
            timeout=(1, 1),  # 1 second connect, 1 second read
            retries=2,
            backoff_factor=1,
        )
        print("Status:", response.status_code)
    except requests.exceptions.Timeout:
        print("Failed after retries due to timeout.")