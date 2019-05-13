import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybundestag-Jhruzik",
    version="0.0.1",
    author="Joshua Hruzik",
    author_email="joshua.hruzik@gmail.com",
    description="Package to parse Bundestag data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jhruzik/pybundestag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing"
    ],
)