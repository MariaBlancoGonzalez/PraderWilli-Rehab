from setuptools import setup
with open("README.md", "r") as fh:
    README = fh.read()
setup(
    name="Prader Willi",
    version="1.0.0",
    description="Prader Willi Rehab System",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MariaBlancoGonzalez/PraderWilli-Rehab",
    author="Maria Blanco",
    author_email="maria.blanco4@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    packages=["assets", "data", "docs", "src"],
    include_package_data=True,
    install_requires=[
        "pygame", "mediapipe", "opencv-python", "svglib"],
    entry_points={
        "console_scripts": [
            "prader_willi = src.main:main"
        ]
    }
)
