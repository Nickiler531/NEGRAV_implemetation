all: install deploy
	 
install:
#	pip install pynmea2
deploy: 
	python deploy.py
	cp wifi_adhoc_setup.sh /opt/NEGRAV
	cp Negrav_base.py /opt/NEGRAV/
	cp -R ../src /opt/NEGRAV/
clean:
	rm -r /opt/NEGRAV
