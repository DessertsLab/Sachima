# make sure you installed wheel
# python3 -m pip install --user --upgrade setuptools wheel

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*




git tag -a 2020.8.29.1 -m '2020.8.29.1'
git push origin --tags


# remove remote tag

# git push origin --delete tag 2020.5.9