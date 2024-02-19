rm -rf dist build prompthub.egg-info/
python setup.py bdist_wheel
twine upload dist/*
