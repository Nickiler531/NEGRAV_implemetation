all: install deploy1
	 
install:
	pip install pynmea2

deploy1: 
	python deploy.py 1
	cp wifi_adhoc_setup.sh /opt/NEGRAV
	cp Negrav_node.py /opt/NEGRAV/Negrav_node.py
	cp -R ../src /opt/NEGRAV/

deploy2:
	python deploy.py 2
	cp wifi_adhoc_setup.sh /opt/NEGRAV
	cp Negrav_node.py /opt/NEGRAV/Negrav_node.py
	cp -R ../src /opt/NEGRAV/

deploy3:
	python deploy.py 3	
	cp wifi_adhoc_setup.sh /opt/NEGRAV
	cp Negrav_node.py /opt/NEGRAV/Negrav_node.py
	cp -R ../src /opt/NEGRAV/

clean:
	rm -r /opt/NEGRAV
