python3 setup.py sdist bdist_wheel

python3 -m twine upload dist/*



git tag -a 2019.3.6 -m '2019.3.6'
git push origin --tags

# remove remote tag

git push origin --delete tag 2019.3.6