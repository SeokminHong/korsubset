from setuptools import find_packages, setup


setup(
    name="kor-subset",
    version="0.1",
    description="An easy font subsetting tool for Korean fonts.",
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
