python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*



git tag -a 2019.3.7 -m '2019.3.7'
git push origin --tags

# remove remote tag

git push origin --delete tag 2019.3.7