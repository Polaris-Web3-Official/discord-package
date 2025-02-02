# discord-package/setup.py
from setuptools import setup, find_packages

setup(
    name='discord-package',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dcp=src.cli:main',
        ],
    },
    install_requires=[
        'discord.py',
        'watchdog',
        'asyncio',
        'datetime',
        'requests',
        'rich',
    ],
    description='A packager to create and manage Discord bots easily (in Windows)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MrWiki15/discord-package', 
    author='Wilkenson Canton',
    author_email='mrwiki@cusoft.tech',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
