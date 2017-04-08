## rslide

`rslide` is a tool to gradually lower the [Redis](https://redis.io)
maxmemory directive.

Redis is single threaded and lowering the maximum memory below the used
level will cause the database to enter a blocking eviction loop until the
database fits within the new maxmemory value.

This is useful when for ex.  when reducing the amount of volatile data in
a redis database with a mixed keyspace (ie. not all data is volatile)
before slaving or migrating the data somewhere else.

## Setup

### from PyPI

    $ pip install redis-memslider
    $ rslide ...

### from source

    $ git clone git@github.com:steinnes/redis-memslider.git
    $ cd redis-memslider
    $ make
    $ rslide ...


## Example usage/output:

    $ rslide -r 1073741824 -s 20 -i 1
    About to reduce maxmemory from 4294967296 -> 3221225472 in 20 steps of 53687091, with 1s intervals, continue? [Y/n]
    Setting maxmemory to 4241280205: took 0.000387191772461s
    Setting maxmemory to 4187593114: took 0.000396013259888s
    Setting maxmemory to 4133906023: took 0.000409841537476s
    Setting maxmemory to 4080218932: took 0.000411987304688s
    Setting maxmemory to 4026531841: took 0.000408172607422s
    Setting maxmemory to 3972844750: took 0.000454902648926s
    Setting maxmemory to 3919157659: took 0.000378131866455s
    Setting maxmemory to 3865470568: took 0.000229835510254s
    Setting maxmemory to 3811783477: took 0.000398874282837s
    Setting maxmemory to 3758096386: took 0.000397920608521s
    Setting maxmemory to 3704409295: took 0.000212907791138s
    Setting maxmemory to 3650722204: took 0.000449180603027s
    Setting maxmemory to 3597035113: took 0.000396013259888s
    Setting maxmemory to 3543348022: took 0.000416040420532s
    Setting maxmemory to 3489660931: took 0.000401973724365s
    Setting maxmemory to 3435973840: took 0.000399112701416s
    Setting maxmemory to 3382286749: took 0.000423908233643s
    Setting maxmemory to 3328599658: took 0.000401973724365s
    Setting maxmemory to 3274912567: took 0.000410079956055s
    Setting maxmemory to 3221225476: took 0.000394821166992s
    Setting maxmemory to 3167538385: took 0.000474214553833s

Note how `rslide` actually performs 21 steps, but the second-to-last value
is 4 bytes above the target of 3221225472.  This is because `rslide` will
continue until the new maxmemory setting is below or equal to the target.


## Background

[Changing redis maxmemory gradually](https://steinn.org/post/redis-gradual-maxmemory/)
