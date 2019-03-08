python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*



git tag -a 19.3.1 -m '19.3.1'
git push origin --tags

# remove remote tag

git push origin --delete tag 19.3.1