from setuptools import setup, find_packages

setup(
    name='Wednesdays-Wicked-Adventures',
    version='1.0.dev0',
    packages=find_packages(where='main'),
    package_dir={'': 'main'},
    py_modules=['config'],
    include_package_data=True,
    install_requires=[
        'Flask==3.1.2',
        'flask-sqlalchemy==3.1.1',
        'SQLAlchemy-Utils==0.42.1',
        'PyMySQL==1.1.2',
        'flask-login==0.6.3',
        'Flask-Admin==1.6.1',
        'WTForms==3.1.2'
    ],
    python_requires='>=3.9',
)
