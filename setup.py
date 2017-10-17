import os


from setuptools import setup
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="openbaton-ems",
    version="1.0.1",
    author="Openbaton",
    author_email="dev@openbaton.org",
    description="Openbaton generic EMS",
    license="Apache 2.0",
    keywords="python ems vnfm openbaton open baton",
    url="http://openbaton.github.io/",
    packages=["ems"],
    install_requires= ["pika", "gitpython"],
    long_description="Element management system that works in conjuction Openbaton Generiv-VNFM",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: Apache Software License"
    ],
    scripts = ["add-upstart-ems"],
    entry_points={
        'console_scripts': [
            'openbaton-ems = ems.ems:main'
        ]
    },
    data_files=[("/opt/openbaton/ems/upstart", ["etc/openbaton/init.d/openbaton-ems-debian", "etc/openbaton/init.d/centos-upstart"]),]
)
