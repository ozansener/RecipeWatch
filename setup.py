from setuptools import setup, find_packages

setup(
		name='RecipeWatch',
		version='0.0.1',
		author="Ozan Sener",
		author_email="os79@cornell.edu",
		description="Understanding Recipes from Multi-Modal Large Scale Data",
		packages=find_packages(),
		include_package_data=True,
		install_requires=[
			'numpy',
			'scipy',
			'pandas',
			'scikit-learn',
			'pymongo',
			'pysrt'
		]
)
