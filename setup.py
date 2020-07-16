from setuptools import setup, find_namespace_packages, find_packages

setup(
    name="oscope",
    version='0.1',
    description="Python wrapper for oscope VISA commands.",
    author="Sequoia Ploeg",
    author_email="sequoiap4@gmail.com",
    url="https://github.com/byucamacholab/oscope",
    packages=find_packages(),
    package_dir={
        '': 'src',
    }
)