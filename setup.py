from setuptools import setup, find_packages
setup(
    name = "vbox-tray",
    version = "0.1",
    packages = find_packages(),
    scripts = ["vbox-tray.py"],

    install_requires = ["trayify"],

    package_data = {
        'vboxtray': ['*.py'],
    },

    # metadata for upload to PyPI
    author = "kiij",
    description = "Tray icon for VirtualBox",
    license = "MIT",
    keywords = "virtualbox system tray gtk",
    url = "https://github.com/kiij/vbox-tray",
)