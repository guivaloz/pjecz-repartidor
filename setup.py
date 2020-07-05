from setuptools import setup

setup(
    name='PJECZ Repartidor',
    version='1.0',
    py_modules=[
        'repartidor',
    ],
    install_requires=[
        'Click',
        'tabulate',
    ],
    entry_points="""
        [console_scripts]
        repartidor=repartidor:cli
        """,
)
