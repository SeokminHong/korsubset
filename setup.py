from setuptools import find_packages, setup
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="korsubset",
    version="0.1",
    description="An easy font subsetting tool for Korean fonts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SeokminHong/korsubset",
    author="Seokmin Hong",
    author_email="ghdtjrals240@naver.com",
    license="MIT",
    packages=find_packages(),
    package_data={"korsubset": ["unicode-range.txt"]},
    zip_safe=False,
    install_requires=["fonttools", "Brotli", "zopfli"],
    keywords=["font", "Korean", "Hangul", "subset"],
    entry_points={"console_scripts": ["korsubset=korsubset.__main__:main"]},
)
