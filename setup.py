from setuptools import setup, find_packages

setup(
    name="ckd-predictor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.1",
        "joblib==1.0.1",
        "numpy==1.21.0",
        "pandas==1.3.0",
        "scikit-learn==0.24.2",
        "gunicorn==20.1.0"
    ],
    python_requires=">=3.9",
)