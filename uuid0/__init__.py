r"""Better timestamped UUID objects (UUID0).

This module provides immutable UUID objects (class UUID), the function
generate() for generating (non-standard) timestamped UUIDs and the helper
functions get_ts(), get_unix_ts(), get_datetime() and get_datetime_local()
to extract the timestamp from a generic uuid.UUID object.

Timestamps are stored as the number of 100 microsecond periods since the
UNIX epoch in the first 6 bytes of the UUID.

Typical usage:

    >>> import uuid0

    # make a UUID based on the current time
    >>> uuid0.generate()
    UUID('0dc7ef03-c534-d288-67b7-34cf4dfa9350')

    # make a UUID from a string of hex digits (braces and hyphens ignored)
    >>> x = uuid0.UUID('{0b7dd8d0-7e40-8360-9322-4a361d7b573f}')

    # extract the datetime from a UUID
    >>> str(x.datetime)
    '2010-01-15 00:00:36'

    # convert a UUID to a string of hex digits in standard form
    >>> str(x)
    '0b7dd8d0-7e40-8360-9322-4a361d7b573f'

    # convert a UUID to a base62 string
    >>> x.base62
    'LgQWTxkOpLyTaEuRAav9D'

    # make a UUID from a base62 string
    >>> uuid0.UUID(base62=x.base62)
    UUID('0b7dd8d0-7e40-8360-9322-4a361d7b573f')

    # get the raw 16 bytes of the UUID
    >>> x.bytes
    b'\x0b}\xd8\xd0~@\x83`\x93"J6\x1d{W?'

    # make a UUID from a 16-byte string
    >>> uuid0.UUID(bytes=x.bytes)
    UUID('0b7dd8d0-7e40-8360-9322-4a361d7b573f')
"""

from .core import *
