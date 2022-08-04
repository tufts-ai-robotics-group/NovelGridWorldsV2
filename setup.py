import setuptools
import os
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as f:
        install_requires = f.read().splitlines()
else:
    install_requires = None

setuptools.setup(
    name="NovelGridWorlds",
    version="2.0.0",
    author="Tufts University",
    author_email="Shivam.Goel@tufts.edu",
    description="NovelGridWorlds V2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/waymao/NovelGridWorldsV2",
    project_urls={
        "Bug Tracker": "https://github.com/waymao/NovelGridWorldsV2/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(
        where='.',
        include=['gym_novel_gridworlds2*'],  # ["*"] by default
    ),
    python_requires=">=3.6",
    install_requires=install_requires
)
