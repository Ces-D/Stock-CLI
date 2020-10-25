from setuptools import setup


def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-16') as req:
        content = req.read()
        requirements = content.split()
    return requirements


setup(name='financetools',
      version='1.0',
      packages=['financetools'],
      include_package_data=True,
      install_requires=read_requirements(),
      entry_points="""
    [console_scripts]
    financetools=financetools.cli:cli
    """)
