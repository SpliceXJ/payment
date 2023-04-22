# /bin/bash

if [ ! -f "runserver.sh" ]
then
    echo "unable to find either runserver.sh"
else
    # make migrations
    python3 manage.py makemigrations

    # migrate
    python3 manage.py migrate

    echo "-----     CREATING API INSTANCES     -----"

    for (( i=8001; i<8004; i++ ))
    do
        # start django server 3 times, map to ports 8001, 8002, 8003
        sudo screen -m -d ./runserver.sh $i
    done

    echo
    echo "-----     CREATED 3 API INSTANCES RUNNING ON    -----"
    echo 
    echo "-----     localhost:8001/     -----"
    echo
    echo "-----     localhost:8002/     -----"
    echo
    echo "-----     localhost:8003/     -----"
    echo
fi

# configure load balancer

if [ ! -f "splicenginx.conf" ]
then
    echo "unable to find splicenginx.conf"
else
    # move nginx config file to /etc/nginx/conf.d/ directory
    sudo cp splicenginx.conf /etc/nginx/conf.d/

    # run nginx test
    sudo nginx -t

    # start / restart nginx
    sudo service nginx restart

    # if server started successfully, then
    echo "load balancer running: access api on:"
    echo
    echo "-----     localhost:8000/     -----"
fi