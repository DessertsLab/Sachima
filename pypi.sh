# make sure you installed wheel
# python3 -m pip install --user --upgrade setuptools wheel

python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*



git tag -a 2019.7.1 -m '2019.7.1'
git push origin --tags

# remove remote tag

git push origin --delete tag 2019.7.1