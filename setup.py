import sys
sys.path.insert(0, '.')
from zl2pdf import __version__

from setuptools import setup


setup(
    name='zl2pdf',
    version=__version__,
    author='hit9',
    author_email='nz2324@126.com',
    description='Port zhuanlan.zhihu.com to PDF',
    license='BSD',
    keywords='zhihu, zhuanlan, pdf',
    url='http://github.com/hit9/zhuanlan2pdf',
    packages=['zl2pdf'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'zl2pdf=zl2pdf.cli:main'
        ]
    },
    install_requires=open("requirements.txt").read().splitlines(),
)
