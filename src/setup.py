from setuptools import setup

setup(
    name="omega_bot",
    version="0.1",
    packages=["omega_bot"],
    install_requires=["kucoin", "pandas", "pyalgotrade", "sklearn", "tensorflow", "joblib", "apscheduler"]
)