from setuptools import setup, find_packages
import twine

VERSION = '0.0.1'
DESCRIPTION = 'A http request library made using sockets'
LONG_DESCRIPTION = 'A library that sends http requests using sockets which is 100x faster than the normal requests library'

# Setting up
setup(
    name="requestsockets",
    version=VERSION,
    author="Issac",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'web surface', 'web scrape', 'http request', 'requests', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)