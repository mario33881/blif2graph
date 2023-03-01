import os
import setuptools

version = "2.0.0"


def get_readme():
    """
    Returns README.md content.
    :return str long_description: README.md content
    """
    long_description = ""
    this_directory = os.path.abspath(os.path.dirname(__file__))

    if os.path.isfile(os.path.join(this_directory, 'README.md')):
        with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
            long_description = f.read()
    else:
        raise Exception("README.md file not found")

    return long_description


if __name__ == '__main__':

    setuptools.setup(
        install_requires=[
            "pygraphviz",
            "blifparser==2.0.1"
        ],  # dependencies
        python_requires='>=3.7',
        packages=setuptools.find_packages(include=['blif2graph']),

        name='blif2graph',  # name of the PyPI-package.
        version=version,    # version number
        author="Zenaro Stefano (mario33881)",
        entry_points={
            "console_scripts": ["blif2graph = blif2graph.blif2graph:main"]
        },
        author_email="mariortgasd@hotmail.com",
        url="https://github.com/mario33881/blif2graph",
        keywords='SIS BLIF Graph',
        license='MIT',
        description='Generate graphs from BLIF files',
        long_description=get_readme(),
        long_description_content_type='text/markdown',
        classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 5 - Production/Stable',

            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: MIT License',

            # Specify the Python versions you support here. In particular, ensure
            # that you indicate whether you support Python 2, Python 3 or both.
            'Programming Language :: Python :: 3',
        ]
    )