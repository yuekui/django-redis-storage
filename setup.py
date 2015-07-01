from os.path import join, dirname

from setuptools import setup


setup(
    name='django_redis_storage',
    version=0.1,
    install_requires=[u'redis>=2.9.0'],
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='',
    url='https://github.com/yuekui/django-redis-storage',
)
