# /bin/bash

if [ ! -f "manage.py" ]
then
    echo "unable to find manage.py" 
else
    # $1 accesses port variable passed when running the command
    python3 manage.py runserver $1
fi