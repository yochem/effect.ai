check:
	pylint -d C0103,C0114,C0115,C0116,W0102 --exit-zero cap/
	mypy --disallow-untyped-defs --disallow-incomplete-defs cap/
	darglint -z short -m "{path}:{line}: {msg}" -v 2 cap/

doc:
	pdoc3 --config show_source_code=False --config latex_math=True --html cap/ -o docs/ --force
	mv -f docs/cap/* docs/
	rm -rf docs/cap
