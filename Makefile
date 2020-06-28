check:
	pylint -d C0103,C0114,C0115,C0116,W0102 --exit-zero cap/
	mypy --disallow-untyped-defs --disallow-incomplete-defs cap/
	darglint -z short -m "{path}:{line}: {msg}" -v 2 cap/

doc:
<<<<<<< HEAD
	pdoc3 --config show_source_code=False --config latex_math=True --html cap/ -o docs/ --force
=======
	pdoc3 --config show_source_code=False \
	      --config latex_math=True \
	      --config git_link_template="\"https://github.com/yochem/cap/blob/{commit}/{path}#L{start_line}-L{end_line}\"" \
	      --html cap/ -o docs/ --force
	mv -f docs/cap/* docs/
	rm -rf docs/cap
>>>>>>> origin/master
