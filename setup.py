import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uci_janggi-sprinter89", # Replace with your own username
    version="1.0.0",
    author="Heeseob Kim",
    author_email="sprinter89tv@gmail.com",
    description="A package to interact with fairy-stockfish janggi variant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sprinter89/uci_janggi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires='>=3.8',
)