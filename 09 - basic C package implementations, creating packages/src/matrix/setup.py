from setuptools import setup, Extension
from Cython.Build import cythonize

setup(
    name='matrix',
    version=0.1,
    packages=['matrix'],
    ext_modules=cythonize(
        Extension(
            name='matrix.multiply',
            sources=['matrix/multiply.pyx'],
            include_dirs=["/usr/include/python3.x"],
            libraries=["c"],
        )
    ),
    install_requires=['Cython'],
)
