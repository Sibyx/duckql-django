from setuptools import setup


def read_files(files):
    data = []
    for file in files:
        with open(file) as f:
            data.append(f.read())
    return "\n".join(data)


meta = {}
with open('duckql-django/version.py') as f:
    exec(f.read(), meta)

setup(
    name='duckql-django',
    version=meta['__version__'],
    packages=[
        'duckql_django'
    ],
    install_requires=[
        'pydantic==1.*',
        'click==7.*',
        'typing-extensions'
    ],
    url='https://github.com/Sibyx/duckql-django',
    license='MIT',
    author='Jakub Dubec',
    author_email='jakub.dubec@gmail.com',
    description='duckQL Django bindings',
    long_description=read_files(['README.md', 'CHANGELOG.md']),
    long_description_content_type='text/markdown',
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries',
    ]
)
