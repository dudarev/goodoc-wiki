get:
	python goodoc.py get
make:
	python goodoc.py make
publish:
	cd _site; git add .; git commit -m "update of `date`"; git push
