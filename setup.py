"""Setup script for PCG Tools."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pcg-tools",
    version="2.1.0",
    author="Brian Slater",
    author_email="brian.m.slater@gmail.com",
    description="Cross-platform Korg PCG file editor - Python rewrite of PCG Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bslater/pcg-tools-python",
    project_urls={
        "Bug Reports": "https://github.com/bslater/pcg-tools-python/issues",
        "Source": "https://github.com/bslater/pcg-tools-python",
        "Documentation": "https://github.com/bslater/pcg-tools-python#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="korg, pcg, synthesizer, kronos, oasys, triton, music, audio, editor",
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pcg-tools=pcg_tools.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
