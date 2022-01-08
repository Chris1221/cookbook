import setuptools

setuptools.setup(
    name="cookbook",
    version="1.0",
    author="Chris",
    author_email="chris.c.1221@gmail.com",
    description="A cookbook!",
    install_requires=["flask", "Frozen-Flask"],
    packages=setuptools.find_packages(),
)