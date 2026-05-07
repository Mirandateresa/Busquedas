from setuptools import setup, find_packages

setup(
    name="busquedas",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'Flask==2.3.3',
        'flask-cors==4.0.0',
        'gunicorn==20.1.0',
    ]
)
