from setuptools import setup, find_packages
with open('README.md') as f:
    long_description = f.read()
setup(
    name='fmover',
    version='0.0.1',
    description='Move files based on file properties and given criteria',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ephraim Siegfried',
    author_email='ephraim.siegfried@hotmail.com',
    url="https://github.com/EphraimSiegfried/fmover",
    license="MIT",
    keywords=["filemanager","filemover","mover"],
    package_dir={'fmover': 'fmover'},
    python_requires=">=3.6.0",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Desktop Environment :: File Managers"
    ],
    entry_points={"console_scripts":["fmover = src.fmover.__main__:main"]},
    install_requires=["notifypy>=1.0.3.0", "osxmetadata>=1.2.2", "appdirs"]
)
