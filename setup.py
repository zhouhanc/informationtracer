from setuptools import setup

setup(
    name='informationtracer',
    version='0.1.8',    
    description='Client-side API to access Information Tracer',
    url='https://github.com/zhouhanc/informationtracer',
    author='Zhouhan Chen',
    author_email='zhouhan.chen@nyu.edu',    
    license='BSD 2-clause',
    packages=['informationtracer'],
    install_requires=['requests',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)    
