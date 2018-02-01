#!/usr/bin/env python
from distutils.core import setup
from distutils.command.install_data import install_data
import pprint
import glob
import os.path

# This is hacky, but it means install_requires can be defined below.
with open(os.path.abspath('pych/version.py'), 'r') as fp:
    version_py_content = fp.read()
APP_NAME = None
APP_VERSION = None
for line in version_py_content.splitlines():
    if line.startswith('APP_NAME'):
        APP_NAME = line.split("'", 2)[1].strip()
    elif line.startswith('APP_VERSION'):
        APP_VERSION = line.split("'", 2)[1].strip()

class post_install(install_data):
    """Do these things post-installation."""

    def run(self):
        """Update the config-file with to match the installed location."""

        install_data.run(self)  # Do whatever install_data used to do

                                # Then modify the installed pych.json
        for filename in self.outfiles:
            if 'pych.json' in filename:
                with open(filename, 'r') as conf_fd:
                    pych_json = conf_fd.read()
                    pych_json = pych_json.replace(
                        "/tmp/pych_dev",
                        self.install_dir
                    )
                with open(filename, 'w') as conf_fd:
                    conf_fd.write(pych_json)

setup(
    name        = APP_NAME,
    version     = APP_VERSION,
    description = 'pyChapel: The Python/Chapel integration module',
    url         = 'http://pychapel.readthedocs.io/',
    author      = 'Simon A. F. Lund',
    author_email='safl@safl.dk',
    maintainer  = 'Chapel Developers',
    maintainer_email = 'chapel_info@cray.com',
    license     = 'Apache 2.0',
    data_files  = [
        ('share/pych/config', ['configs/pych.json']),
        
        ('share/pych/include', glob.glob('include/*.h')),
        ('share/pych/lib', glob.glob('lib/*')),

        ('share/pych/examples', glob.glob('../docs/source/examples/*.py')),
        ('share/pych/examples', glob.glob('../docs/source/examples/*.c')),
        ('share/pych/examples', glob.glob('../docs/source/examples/*.chpl')),
        
        ('share/pych/examples/aux', glob.glob('../docs/source/examples/aux/*.txt')),

        ('share/pych/sfiles/c',      glob.glob('../docs/source/examples/sfiles/c/*')),
        ('share/pych/sfiles/chapel', glob.glob('../docs/source/examples/sfiles/chapel/*')),
        ('share/pych/sfiles/python', glob.glob('../docs/source/examples/sfiles/python/*')),

        ('share/pych/bfiles/c',      glob.glob('../docs/source/examples/bfiles/c/*')),
        ('share/pych/bfiles/chapel', glob.glob('../docs/source/examples/bfiles/chapel/*')),
        ('share/pych/bfiles/python', glob.glob('../docs/source/examples/bfiles/python/*')),

        ('share/pych/templates/c', glob.glob('templates/c/*')),
        ('share/pych/templates/chapel', glob.glob('templates/chapel/*')),
        ('share/pych/templates/python', glob.glob('templates/python/*')),

        ('var/pych/store/c',            ['store/c/empty']),
        ('var/pych/store/chapel',       ['store/chapel/empty']),
        ('var/pych/store/third_party',  ['store/third_party/empty']),

        ('share/pych/testing', glob.glob('testing/*'))
    ],
    packages=['pych'],
    scripts=["scripts/pych"],
    cmdclass=dict(install_data=post_install)
)
