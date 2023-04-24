### getting started

#### 2 ways to run api:
      - run multiple instances of the API, access through load balancer 
      - run single instance
      
### prerequisite for single instance
      - python installed

#### Running single instance steps
      - pip install -r requirements.txt
      - python manage.py runserver in directory root : api runs on localhost:8000
      
### prerequisite for multiple instances
      - linux machine / wsl running
      - python installed
      - nginx installed
     
#### Running single instance steps
      - pip install -r requirements.txt
      - run ./runloadbalancer.sh in directory root : api runs on localhost:8000
