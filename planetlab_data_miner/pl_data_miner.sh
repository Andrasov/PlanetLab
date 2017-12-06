#!/bin/bash

nor=$(cat nor.txt) 
let nor=$nor+1  
echo "$nor" > nor.txt
number_of_runs=$(cat nor.txt)


#------------GENERAL GUI SETINGS-------------
HEIGHT=23
WIDTH=43
BACKTITLE="Data miner for Planetlab"
#------------GUI SETINGS MENUS-------------

main_menu_gui () {

	CHOICE_HEIGHT=5
	TITLE="MAIN MENU"
	MENU="Choose one of the following options:"

	OPTIONS=(1 "Search nodes"
			 2 "Scrap planetlab.eu"
	         3 "Measure Menu"
	         4 "Map Menu"
	         5 "Settings")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in

			1)
				
				node_menu
				main_menu_gui;;

	        2)
	            
	            pl_down
	            main_menu_gui;;
	        3)
	            
	            measure_menu
	            main_menu_gui;;
	        4)
	            
	            map_menu
	            main_menu_gui;;

	        5)	
				settings_menu
				main_menu_gui;;    
	esac

}

settings_menu () {
	
	CHOICE_HEIGHT=6
	TITLE="SETTINGS MENU"
	MENU="Choose one of the following options:"

	OPTIONS=(1 "PL login"
	         2 "PL password"
	         3 "Slice login"
	         4 "Choose SSH key"
	         5 "set defalut")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in
	        1)
	            
	            pl_name_input
	            settings_menu;;
	        2)	
				
	            pl_pass_input
	            settings_menu;;
	        3)	
				
	            sl_name_input
	            settings_menu;;
	    
	        4) 
	        	
	        	ssh_input
	        	settings_menu;;	 

	        5) 
	        	set_defalut
	        	settings_menu;;	
	esac

}

measure_menu () {

	CHOICE_HEIGHT=4
	TITLE="MEASURE MENU"
	MENU="Choose one of the following options:"

	OPTIONS=(
	         1 "set cron"
	         2 "specify measured elements")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in
	        
	        1)
	            set_cron
	            measure_menu;;
	        2)
				set_elements
				build_script_for_cron
				measure_menu;;    
	esac

}

map_menu () {

	CHOICE_HEIGHT=4
	TITLE="MAP MENU"
	MENU="Choose one of the following options:"

	OPTIONS=(1 "Generate map"
	         2 "Select map elements")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in
	        1)	
				generate_map
				map_menu;;
	        2)
	            map_elements
	            map_menu;;
	       
	esac
}

set_cron () {


	CHOICE_HEIGHT=4
	TITLE="crontab menu"
	MENU="Choose one of the following options:"

	OPTIONS=(1 "set measuremend daily"
	         2 "set measuremend weekly"
	         3 "set measuremend monthly"
	         4 "remove all measuremend from cron")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in
	        1)
	            daily
	            set_cron;;

	        2)
	            weekly
	            set_cron;;

	        3)
				monthly
				set_cron;;    

	        4)
				remove_cron
				set_cron;;    
	esac



}

selected_choice () {

	CHOICE_HEIGHT=3
	TITLE="node menu"
	MENU=$(cat choice_info.txt)

	OPTIONS=(1 "connect via SSH"
	         2 "connect via MC"
	         3 "show on map")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in
	        1)
	 			connect_ssh
	 			selected_choice;;

	        2)
	            connect_mc
	            selected_choice;;

	        3)
				show_node
				selected_choice;;
   
	esac
}


node_menu () {
	sr_choice=""
	CHOICE_HEIGHT=3
	TITLE="node menu"
	MENU=

	OPTIONS=(1 "search by DNS"
	         2 "search by IP"
	         3 "search by location")

	CHOICE=$(dialog --clear \
	                --backtitle "$BACKTITLE" \
	                --title "$TITLE" \
	                --menu "$MENU" \
	                $HEIGHT $WIDTH $CHOICE_HEIGHT \
	                "${OPTIONS[@]}" \
	                2>&1 >/dev/tty)
	clear
	case $CHOICE in
	        1)
				sr_choice=3
	 			search_nodes;;

	        2)
	            sr_choice=2
	 			search_nodes;;

	        3)
				sr_choice=4
				search_by_loc;;
   
	esac
}




#------------GUI SETINGS CHECKBOXES-------------

map_elements(){
	map_setter=""
	CHOICE_HEIGHT=2
	TITLE="Map elements menu"
	CHECKLIST="choose what to display on map(SPACE toggle ON/OFF):"

	
options=(1 "ICMP responds" off   
         2 "SSH time" off)

cmd=(dialog --separate-output --checklist \
	"$CHECKLIST" $HEIGHT $WIDTH $CHOICE_HEIGHT)


choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
clear
for choice in $choices
do
    case $choice in
        1)	map_ele_icmp
            ;;
        2)	map_ele_ssh
            ;;
        
    esac
done

}

set_elements(){

	cron_setter=""
	CHOICE_HEIGHT=3
	TITLE="set elements to monitor"
	CHECKLIST="choose what to monitor(SPACE toggle ON/OFF):"

	options=(1 "ICMP responds" off
			 2 "SSH time" off
			 3 "Ignore non responsive servers" off)

	cmd=(dialog --separate-output --checklist \
	"$CHECKLIST" $HEIGHT $WIDTH $CHOICE_HEIGHT)

	choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
clear
for choice in $choices
do
    case $choice in
        1)
			cron_setter_1
            ;;
        2)
			cron_setter_2
            ;;
        
    esac
done


	
}


#------------GUI SETINGS YESNO BOXES-------------


set_defalut(){

	TITLE="warning"
	YESNO="This is going to set defalut logins,passwords and ssh key"

	dialog --clear \
		   --backtitle "$BACKTITLE" \
		   --title "$TITLE" \
		   --yesno	"$YESNO" \
		   $HEIGHT $WIDTH \

	case $? in
  		0)
    		defalut_settings
    		;;
  		1)
    		echo "No chosen."
    		;;
  		255)
    		echo "ESC pressed."
    		;;
		esac

	clear
}

pl_down(){

	TITLE="warning"
	YESNO="This is going to take around 1 hour are you sure ?"

	dialog --clear \
		   --backtitle "$BACKTITLE" \
		   --title "$TITLE" \
		   --yesno	"$YESNO" \
		   $HEIGHT $WIDTH \

	case $? in
  		0)
    		download_planet
    		;;
  		1)
    		echo "No chosen."
    		;;
  		255)
    		echo "ESC pressed."
    		;;
		esac

	clear
}

#------------GUI SETINGS USER INPUTS-------------

user_input(){

	OUTPUT="/tmp/input.txt"
	dialog --clear \
		   --backtitle "$BACKTITLE" \
		   --title "$TITLE" \
		   --inputbox "$INPUTBOX" \
		   $HEIGHT $WIDTH \
		   2>$OUTPUT

	input=$(<$OUTPUT)

	trap "rm $OUTPUT; exit" SIGHUP SIGINT SIGTERM
	rm $OUTPUT
	clear

}

pass_input(){

	OUTPUT="/tmp/input.txt"
	dialog --clear \
		   --backtitle "$BACKTITLE" \
		   --title "$TITLE" \
		   --backtitle "$BACKTITLE" \
		   --passwordbox "$PASSBOX" \
		   $HEIGHT $WIDTH \
		   2>$OUTPUT

	pass=$(<$OUTPUT)

	trap "rm $OUTPUT; exit" SIGHUP SIGINT SIGTERM
	rm $OUTPUT
	clear
}

fselecte() {

dir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)

	OUTPUT="/tmp/input.txt"
	dialog --clear \
	--backtitle "$BACKTITLE" \
	--title "ssh key" \
	--stdout \
	--title "Please choose a ssh key" \
	--fselect $dir 14 48 2>$OUTPUT

	fil=$(<$OUTPUT)
	
	trap "rm $OUTPUT; exit" SIGHUP SIGINT SIGTERM
	rm $OUTPUT
	clear

#
#	OUTPUT="/tmp/input.txt"
#	dialog --clear \
#		   --title "$TITLE" \
#		   --stdout \
#		   --fselect $pwd \
#		   $HEIGHT $WIDTH \
#		    2>$OUTPUT
#
#	fil=$(<$OUTPUT)
#	trap "rm $OUTPUT; exit" SIGHUP SIGINT SIGTERM
#	rm $OUTPUT
#	clear
}

search_input() {

	TITLE="search"
	INPUTBOX="search for:"
	user_input
	sr_input=$input
}

pl_name_input(){

	TITLE="WEB login"
	INPUTBOX="Login for Planetlab:"
	user_input
	pl_name=$input
}

sl_name_input(){

	TITLE="Slice login"
	INPUTBOX="Login to PL servers:"
	user_input
	sl_name=$input
}

pl_pass_input(){

	TITLE="WEB Password"
	PASSBOX="Password:"
	pass_input
	pl_pass=$pass
}

ssh_input(){

	TITLE="SSH key"
	fselecte
	ssh_key=$fil
}



#-----------BACKEND----------------
#---variables-----
path=$(pwd)
planet_data=$(find $path -type f -name "*.node")


#---functions-----


#---check the internet-------

is_it_on () {

if ping -q -c 1 -W 1 8.8.8.8 >/dev/null
	then
	  	echo "ok"
	else
	 	 dialog --title "ERROR" --msgbox 'No internet connection detected ! program will not work properly ' $HEIGHT $WIDTH
	fi


}

first_run() {

	 	 dialog --title "Hello" --msgbox "$(cat bin/hello.txt)" $HEIGHT $WIDTH


}


#---search nodes functions-------------------------------------------------------------------------------------------------
 #boh pomahaj tomu kto to bude chciet pochopit,v podstate google search autocomplete v bashi, ked som to pisal mal som v tele vela kofeinu
search_nodes(){

	search_input

	if [ -z "$sr_input" ]
		then
	    	echo "VAR is empty"
	    	main_menu_gui

		else
			build_sr_out
			generate_node_info
			selected_choice
	fi	

	#rm choice_info.txt choice_temp.txt
	trap "rm choice_temp.txt choice_info.txt; exit" SIGHUP SIGINT SIGTERM
	sr_choice=""
}

build_sr_out(){

	counter=1

	cat $path/bin/search_nodes_prebuild.dat > search_function.sh

	cat $planet_data | cut -f$sr_choice | awk 'NR>1' | \
	grep $input | head -10 | while read line

	do 
		echo "\"$line\" \"$counter\" \\" >> search_function.sh
		let counter=counter+1
	done


	cat $path/bin/search_nodes_postbuild.dat >> search_function.sh

	chmod +x search_function.sh
	./search_function.sh
	rm search_function.sh 
}

build_sr_out_specy(){

	counter=1

	cat $path/bin/search_nodes_prebuild.dat > search_function.sh

	cat $planet_data | cut -f$sr_choice | awk 'NR>1' | sort | uniq \
	| while read line

	do 
		echo "\"$line\" \"$counter\" \\" >> search_function.sh
		let counter=counter+1
	done


	cat $path/bin/search_nodes_postbuild.dat >> search_function.sh

	chmod +x search_function.sh
	./search_function.sh
	rm search_function.sh 
}

build_sr_out_specy_2(){

	counter=1

	cat $path/bin/search_nodes_prebuild.dat > search_function.sh

	cat $planet_data  | awk 'NR>1'|grep $choice |cut -f$sr_choice | sort | uniq \
	| while read line

	do 
		echo "\"$line\" \"$counter\" \\" >> search_function.sh
		let counter=counter+1
	done


	cat $path/bin/search_nodes_postbuild.dat >> search_function.sh

	chmod +x search_function.sh
	./search_function.sh
	rm search_function.sh 
}

search_by_loc (){
build_sr_out_specy
choice=$(cat choice_temp.txt)
rm choice_temp.txt
sr_choice=5
build_sr_out_specy_2
choice=$(cat choice_temp.txt)
rm choice_temp.txt
sr_choice=3
build_sr_out_specy_2
generate_node_info
selected_choice
sr_choice=""

rm choice_info.txt choice_temp.txt
trap "rm choice_temp.txt choice_info.txt; exit" SIGHUP SIGINT SIGTERM

}

generate_node_info(){
	# useless use of cat gonna fix someday

	echo "getting data"

	choice=$(cat choice_temp.txt)

	node=$(cat $planet_data | grep $choice | cut -f3)
	node_ip=$(cat $planet_data | grep $choice | cut -f2)
	continent=$(cat $planet_data | grep $choice | cut -f4)
	country=$(cat $planet_data | grep $choice | cut -f5)
	region=$(cat $planet_data | grep $choice | cut -f6)
	city=$(cat $planet_data | grep $choice | cut -f7)
	URL=$(cat $planet_data | grep $choice | cut -f8)
	name=$(cat $planet_data | grep $choice | cut -f9)
	lat=$(cat $planet_data | grep $choice | cut -f10)
	long=$(cat $planet_data | grep $choice | cut -f11)


	fping -C 2  -q $node_ip &> fpingout.txt
	icmp=$(cat fpingout.txt | awk '{print$4}')
	rm fpingout.txt

	echo "
	NODE: $node
	IP: $node_ip
	CONTINENT: $continent
	COUNTRY: $country
	REGION: $region
	CITY: $city
	URL: $url
	FULL NAME: $name
	LATITUDE: $lat  
	LONGITUDE: $long 
	ICMP RESPOND (NOW): $icmp" >choice_info.txt

}

#----end of search functions-------------------------------------------------------------------------------------
cron_setter_1(){

	cron_setter="1"

}

cron_setter_2(){

	cron_setter="${cron_setter}2"
}

daily(){

	 crontab -l | { cat; echo "@daily ${path}/bin/cron_script.sh"; } | crontab -

}

weekly(){

	crontab -l | { cat; echo "@weekly ${path}/bin/cron_script.sh"; } | crontab -
}

monthly(){

	crontab -l | { cat; echo "@monthly ${path}/bin/cron_script.sh"; } | crontab -
}

remove_cron(){

	crontab -l | grep -v cron_script | crontab -
}

build_script_for_cron(){

	rm cron_script.sh
	touch cron_script.sh
	chmod +x cron_script.sh

	echo "sl_name=$sl_name" >> cron_script.sh
	echo "ssh_key=$ssh_key" >> cron_script.sh

	if [ "$cron_setter" == "1" ]
		then
			cat $path/bin/icmp_build.dat >> cron_script.sh
			cat $path/bin/cron_postbuild_1.dat >> cron_script.sh
	fi

	if [ "$cron_setter" == "2" ]
		then
			cat $path/bin/ssh_build.dat >> cron_script.sh
			cat $path/bin/cron_postbuild_2.dat >> cron_script.sh

	fi			

	if [ "$cron_setter" == "12" ]
		then
			cat $path/bin/ssh_build.dat >> cron_script.sh
			cat $path/bin/icmp_build.dat >> cron_script.sh
			cat $path/bin/cron_postbuild_12.dat >> cron_script.sh

	fi			
}

defalut_settings(){

	pl_name="studentutko@gmail.com"
	pl_pass="b^tSu265t:Tk"
	sl_name="cesnetple_vut_utko"
	ssh_key="$path/bin/utko_planetlab"

}

connect_ssh(){

	echo "trying to conncet to $node via SSH"
	ssh $sl_name@$node \
		-o "PreferredAuthentications=publickey"\
    	-o "PasswordAuthentication=no"\
    	-o "ConnectTimeout=20"\
    	-o "UserKnownHostsFile=/dev/null"\
    	-o "StrictHostKeyChecking=no"\
    	-o "IdentityFile=$path/bin/utko_planetlab"
}

connect_mc(){

	echo "trying to conncet to $node via GNU midnight commander"
	ssh-add $ssh_key
	mc sh://$sl_name@$node:/home
}

show_node(){

	python3 $path/python_scripts/map_one.py $lat $long $node

	python -m webbrowser "map_1.html" > /dev/null 2>&1

	trap "rm map_1.html ; exit" SIGHUP SIGINT SIGTERM
}

map_ele_ssh(){

	map_setter="${map_setter}2"
}

map_ele_icmp(){

	map_setter=1
}

generate_map(){

	if [ "$map_setter" == "1" ]
		then
		data_prep_icmp
		python3 $path/python_scripts/icmp_map.py	
		python -m webbrowser "map_icmp.html" > /dev/null 2>&1
	fi

	if [ "$map_setter" == "2" ]
		then
		data_prep_ssh
		python3 $path/python_scripts/ssh_map.py	
		python -m webbrowser "map_ssh.html" > /dev/null 2>&1
	fi			

	if [ "$map_setter" == "12" ]
		then
		data_prep_full
		python3 $path/python_scripts/full_map.py	
		python -m webbrowser "map_full.html" > /dev/null 2>&1
	fi			

	
}

data_prep_icmp(){

	cat $planet_data| awk 'NR>1' |sort| uniq| cut -f10,11,3 | sort -k2 -u > python_scripts/base_data.txt
}

data_prep_ssh (){

	cat $planet_data| awk 'NR>1' |sort| uniq| cut -f10,11,3 | sort -k2 -u > python_scripts/base_data.txt

}

data_prep_full(){

	cat $planet_data| awk 'NR>1' |sort| uniq| cut -f10,11,3 | sort -k2 -u > python_scripts/base_data.txt

}

download_planet(){

	python3 $path/python_scripts/planetlab_list_creator.py -u $pl_name -p $pl_pass -e
}

run_full_measure(){

	echo "running full measure wait please"
	cat $planet_data |awk 'NR>1'| cut -f2 > IP.txt
	echo "testing ICMP responces"
	icmp_test
	rm IP.txt

	echo "runing SSH test"
	cat $planet_data |awk 'NR>1'| cut -f3 >hosts.txt
	ssh_test
	rm hosts.txt

}


icmp_test(){

	fping -C 2 -q < IP.txt  &> fpingout_all.txt

}

ssh_test (){

	pssh -h hosts.txt -l $sl_name\
		-O "PreferredAuthentications=publickey"\
    	-O "PasswordAuthentication=no"\
    	-O "UserKnownHostsFile=/dev/null"\
    	-O "StrictHostKeyChecking=no"\
    	-O "IdentityFile=$path/bin/utko_planetlab"\
    	-t 0\
    	-o ssh_tst_out.txt\
    	-i "hostname"

}

#-----RUNING-----------

defalut_settings #for testing, can be commented out 

if [ "$number_of_runs" == "1" ]
	then
	
		first_run
fi		

is_it_on
main_menu_gui
rm map_1.html map_full.html map_ssh.html map_icmp.html map_ssh.html map_full.html python_scripts/base_data.txt  vega.json \
choice_info.txt choice_temp.txt > /dev/null 2>&1
rm full_measure.sh > /dev/null 2>&1





#---------------------------------------------------------------------------

# olesakova zuzana 