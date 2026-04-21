from setuptools import setup, find_packages

setup(
    name="ipmd",
    version="1.2.2",
    description="Image Pixel MetaData - Pin metadata into image pixels",
    author="777Tu",
    packages=["ipmd"],
    package_data={"ipmd": ["*.py"]},
    install_requires=["pillow"],
    
)
