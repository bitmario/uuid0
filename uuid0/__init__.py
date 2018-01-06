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

import os
import uuid
import time
import struct
from datetime import datetime

import base62 as b62


class UUID(uuid.UUID):
    """
    A class that offers a simple, but effective, way to deal with time-based UUIDs.
    Additional encoding methods are included to make UUIDs easier to use with web apps.

    The first 6 bytes of the UUID are an unsigned integer containing the number of 
    1/10000s periods since the UNIX epoch, the remaining bits are random (aside from
    the UUID version).
    This approach offers semi-sequential UUIDs (easy on your indexes), which include
    the creation time but don't include any machine-specific information. 
    """

    def __init__(self, hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None, base62=None):
        r"""Create a UUID0 from either a string of 32 hexadecimal digits,
        a string of 16 bytes as the 'bytes' argument, a string of 16 bytes
        in little-endian order as the 'bytes_le' argument, a tuple of six
        integers (32-bit time_low, 16-bit time_mid, 16-bit time_hi_version,
        8-bit clock_seq_hi_variant, 8-bit clock_seq_low, 48-bit node) as
        the 'fields' argument, a single 128-bit integer as the 'int'
        argument or a base62 string as the 'base62' argument.  When a string
        of hex digits is given, curly braces, hyphens, and a URN prefix are
        all optional.  For example, these expressions all yield the same UUID:

        UUID('{12345678-1234-5678-1234-567812345678}')
        UUID('12345678123456781234567812345678')
        UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
        UUID(bytes='\x12\x34\x56\x78'*4)
        UUID(bytes_le='\x78\x56\x34\x12\x34\x12\x78\x56' +
                      '\x12\x34\x56\x78\x12\x34\x56\x78')
        UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
        UUID(int=0x12345678123456781234567812345678)
        UUID(base62='YLmNWW2NwaipfRR50HIPA')

        Exactly one of 'hex', 'bytes', 'bytes_le', 'fields', 'int' or 
        'base62' must be given. The 'version' argument is optional; if 
        given, the resulting UUID will have its variant and version set
        according to RFC 4122, overriding the given 'hex', 'bytes', 
        'bytes_le', 'fields', 'int' or 'base62'.
        """
        if base62:
            return super().__init__(int=b62.decode(base62), version=version)
        return super().__init__(hex, bytes, bytes_le, fields, int, version)

    @property
    def base62(self) -> str:
        """Get the UUID as a base62 encoded string"""
        return b62.encode(self.int)

    @property
    def ts(self) -> int:
        """Get the timestamp as the number of 100 microsecond periods since the UNIX epoch"""
        return get_ts(self)

    @property
    def unix_ts(self) -> float:
        """Get the UNIX timestamp"""
        return get_unix_ts(self)

    @property
    def datetime(self) -> datetime:
        """Get the timestamp as UTC datetime"""
        return get_datetime(self)

    @property
    def datetime_local(self):
        """Get the timestamp as local datetime"""
        return get_datetime_local(self)


def generate(ts: float=None) -> UUID:
    """Generate a new UUID. If the UNIX timestamp 'ts' is not given, the current time is used"""
    if not ts:
        ts = time.time()
    tsi = int(ts * 10000)
    t_bytes = struct.pack('>Q', tsi)[2:] # pack as an 8-byte uint and drop the first 2 bytes
    r_bytes = os.urandom(10)

    return UUID(bytes=t_bytes + r_bytes)


def get_ts(uid: uuid.UUID) -> int:
    """Returns the timestamp as the number of 100 microsecond periods since the UNIX epoch"""
    time_part = uid.bytes[0:6]
    ts = struct.unpack('>Q', b'\x00\x00' + time_part)
    return ts[0]


def get_unix_ts(uid: uuid.UUID) -> float:
    """Returns the timestamp as UNIX time"""
    return get_ts(uid) / 10000.0


def get_datetime(uid: uuid.UUID) -> datetime:
    """Return the timestamp as UTC datetime"""
    return datetime.utcfromtimestamp(get_unix_ts(uid))


def get_datetime_local(uid: uuid.UUID) -> datetime:
    """Return the timestamp as local datetime"""
    return datetime.fromtimestamp(get_unix_ts(uid))
