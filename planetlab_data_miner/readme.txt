Hello, this is readme file for planetlab_data_miner,
program is loaded with mesurements therefore there is some initial data to display

---INSTALATION----

1. unzip planet_lab_data_miner.zip to desired location 

2. run install.sh
	chmod +x install.sh (needs to be root)
	./install.sh

3. install missing dependencies
	follow the dependencies section

4. run planetlab_data_miner.sh
	chmod +x planetlab_data.miner.sh (needs to be root)
	./planetlab_data_miner.sh


---INSTALLING THE MISSING DEPENDENCIES----

--

---python3---

for ubuntu like distros:

	$ sudo apt-get update
	$ sudo apt-get -y upgrade
	$ sudo apt-get install -y python3-pip

	

for debian like distros:

	$ sudo yum install yum-utils
	$ sudo yum-builddep python
	$ curl -O https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
	$ tar xf Python-3.5.0.tgz
	$ cd Python-3.5.0
	$ ./configure
	$ make
	$ sudo make install


--fping--

ubuntu:

	$sudo apt-get install fping

debian:

	wget http://fping.org/dist/fping-3.13.tar.gz
	tar -xvzf fping-3.13.tar.gz
	cd fping-3.13
	./configure 
	make && make install

---vincent/folium/pandas/numpy/pssh----

sudo pip install vincet
sudo pip install folium
sudo pip install numpy
sudo pip install pandas
sudo pip install pssh




--bugs---

there is ocasional crashes when searching nodes by IPs or by location and pressing cancel  button before selecting node

