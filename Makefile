check:
	pylint -d C0103,C0114,C0115,C0116,W0102 --exit-zero cap/
	mypy --disallow-untyped-defs --disallow-incomplete-defs cap/
	darglint -z short -m "{path}:{line}: {msg}" -v 2 cap/

doc:
	pdoc3 --config latex_math=True --html cap/ -o docs/ --force