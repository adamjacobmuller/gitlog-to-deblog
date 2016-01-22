from setuptools import setup, find_packages

setup(
    name='gitlog-to-deblog',
    version='1.0.0',
    author='Adam Jacob Muller',
    packages=find_packages(),
    author_email='adam@isprime.com',
    entry_points={
        "console_scripts": [
            "gitlog-to-deblog = gitlog_to_deblog.gitlog_to_deblog:main"
        ]
    },
    install_requires=[
        'sh'
    ]
)
