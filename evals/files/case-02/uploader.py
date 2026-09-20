"""Upload helper.

MINI-04 asks for retry behaviour around `perform_upload`. Naming and internal
structure are delegated to the implementer -- see MINI-04.md.
"""


def perform_upload(payload, client):
    """Single attempt. Raises on failure."""
    return client.put(payload)


# TODO(MINI-04): wrap perform_upload so it retries up to three times with a
# growing delay, then re-raises the last error.
