from setuptools import setup, find_packages

setup(
    name='file-mover',
    version='0.0.1',
    description='Move files based on file properties and given criteria',
    author='Ephraim Siegfried',
    author_email='ephraim.siegfried@hotmail.com',
    package_dir={'src': 'src'},
    python_requires=">=3.6.0",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Desktop Environment :: File Managers"
    ],
    entry_points={"console_scripts":["file-mover = src.__main__:main"]},
    install_requires=["notifypy>=1.0.3.0", "osxmetadata>=1.2.2, appdirs~=1.0.3.0"]
)
