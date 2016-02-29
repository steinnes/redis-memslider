import os

from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession

setup(
    name='redis-memslider',
    version='0.1.2',
    description='Gradually reduce redis maxmemory.'
                ''
                'REDIS (redis.io) will block while ensuring maxmemory is honored, so when reducing it significantly'
                'it is helpful to do so over a period of time in smaller steps if necessary.  For example an AWS EC2'
                'm2.2xlarge instance takes in the vicinity of 1-5 seconds to evict 256MB of keys.',
    py_modules=['slider'],
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    url='https://github.com/steinnes/redis-memslider',
    install_requires=[
        str(req.req) for req in
            parse_requirements(
                os.path.join(os.path.dirname(__file__), "requirements.txt"),
                session=PipSession()
            )
    ],
    entry_points='''
        [console_scripts]
        rslide=slider:main
    ''',
)
