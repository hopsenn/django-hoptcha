from setuptools import setup, find_packages

setup(
    name='django-hoptcha',
    version='1.0.0',
    description='Django client integration for the Hoptcha CAPTCHA provider',
    author='Hopsenn',
    author_email='ivan.nikolskiy@hopsenn.com',
    url='https://git.hopsenn.com/hopsenn/django-hoptcha',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.20',
        'Django>=3.2'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
