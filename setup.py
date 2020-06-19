import setuptools


with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='cap',
    version='0.1.0',
    author='Bas de Boer, Anne Kaal, Lysa Ngouateu, Yochem van Rosmalen,' +
    'Florian van der steen',
    author_email='yochem+git@icloud.com',
    description='Create well-formatted captions from ASR files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yochem/cap',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'cap = cap.cli:parse_args'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.7'
)
