from setuptools import setup, find_packages

setup(
    name='gfhelper',
    url='https://github.com/KureFM/gfhelper',
    author='Fukumakoto Kure',
    author_email='kure.fukumakoto@gmail.com',
    version='0.1.0a2',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'Click',
        'ImageHash',
        'PyYAML'
    ],
    entry_points='''
        [console_scripts]
        gfhelper=gfhelper.app:main
    '''

)
