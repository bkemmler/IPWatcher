from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="ip-watcher",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="IP Watcher is a simple web application that periodically scans your network for connected devices and displays them in a web interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ip-watcher",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
