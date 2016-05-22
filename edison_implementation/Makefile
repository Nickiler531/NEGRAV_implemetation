all: install deploy
	 
install:
	pip install pynmea2
deploy: 
	python deploy.py
	cp wifi_adhoc_setup.sh /opt/NEGRAV
	cp Negrav_node.py /opt/NEGRAV/Negrav_node.py
clean:
	rm -r /opt/NEGRAV