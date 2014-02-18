from setuptools import setup, find_packages
setup(
    name = "vbox-tray",
    version = "0.1",
    packages = find_packages(),
    scripts = ["vbox-tray.py"],

    # Purposely left empty. This could contain PyQT or PyGTK, but we're not
    # enforcing that a package be installed on the machine before we can be
    # used. If someone only wants GTK apps, they shouldn't be required to have
    # the PyQT libraries installed as well.
    install_requires = [],

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