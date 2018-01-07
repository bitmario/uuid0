==========================================
uuid0 - better timestamped UUIDs in Python
==========================================

V4 UUIDs are often used as primary keys or as part of database indexes.
However, their random and non-sequential nature can cause locality and 
performance issues.

This Python 3 package mitigates these issues by using encoding a UNIX
timestamp in the first 6 bytes of the UUID, and filling the remaining bytes
with random data. The ``uuid0.UUID`` class inherits from the standard 
``uuid.UUID`` class so it's safe to use all the usual properties (hex, int, 
bytes, etc.)

The package also contains ``uuid0.django`` which provides Django form and
model fields based on the UUID0 type, as well as an abstract ``UUID0Model``.

------
Status
------

This package is in **alpha** status, use at your own risk.

-----
Usage
-----

Install by running::

   pip install uuid0

Example usage::

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

----------------------
What about collisions?
----------------------

Collisions are a concern, of course, but only if you are generating really
**large** amounts of UUIDs in a short timespan.

By default, uuid0 only uses 6 bytes to encode the time and does not encode any
version bits, leaving 10 bytes (80 bits) of random data.

The probability of collision is near zero for most use cases since for each 
1/10000s period, there are 2\ :sup:`80` possible UUIDs.

-----------
Performance
-----------

Generating a UUID0 is slower than generating a UUID v4, but faster than a 
UUID v1.

Below are results for 500k iterations on an i7-6700HQ and Python 3.6.2 
(generated using the ``benchmarks/generate.py`` script):

=================  =========  =========  ========
method             it/s       ?s/it      % slower
=================  =========  =========  ========
uuid.uuid4()       453043     2.207      0.0%
uuid0.generate()   311184     3.214      31.31%
uuid.uuid1()       230163     4.345      49.2%
=================  =========  =========  ========

In terms of database performance, indexes are approximately 18% smaller and
inserts about 23% faster on PostgreSQL with a ``uuid`` type column, but YMMV
depending on your use case.

-------
License
-------

This project is licensed under the MIT License. See the ``LICENSE`` file for
details.
