whereis dialog > /dev/null 2>&1
RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed dialog
[ $RETVAL -ne 0 ] && echo Failure you dont have program dialog

whereis fping > /dev/null 2>&1
RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed fping
[ $RETVAL -ne 0 ] && echo Failure you dont have program fping

whereis pssh > /dev/null 2>&1
RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed pssh
[ $RETVAL -ne 0 ] && echo Failure you dont have program pssh

whereis python3 > /dev/null 2>&1
RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed python3
[ $RETVAL -ne 0 ] && echo Failure you dont have program python3

pip freeze | grep -i vincent > /dev/null 2>&1

RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed vincent
[ $RETVAL -ne 0 ] && echo Failure you dont have installed python lib. vincet

pip freeze | grep -i folium > /dev/null 2>&1

RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed folium
[ $RETVAL -ne 0 ] && echo Failure you dont have installed python lib. folium




pip freeze | grep -i pandas > /dev/null 2>&1

RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed pandas
[ $RETVAL -ne 0 ] && echo Failure you dont have installed python lib. pandas

pip freeze | grep -i numpy > /dev/null 2>&1

RETVAL=$?
[ $RETVAL -eq 0 ] && echo Success you have installed numpy
[ $RETVAL -ne 0 ] && echo Failure you dont have installed python lib. numpy



echo "please follow readme.txt how to install dependencies if you are missing some of the programs"