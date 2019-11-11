# Syncing Bol.com Retailer Shipment Api

### Setup on Local machine (Mac & Linux)

- cd Desktop
- virtualenv bol
- cd bol
- source/bin activate
- mkdir src && cd src

- git clone https://github.com/learnwithcode/Bol-Retailer-Sync-Shipment.git . <=noticeinclude period

- pip install -r requirements.txt
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver

### Setup Celery and RabbitMQ

#### Installing RabbitMQ on MAC

- brew install rabbitmq

#### Installing RabbitMQ on Ubuntu 18.04 LTS

- sudo apt-get install -y erlang
- sudo apt-get install rabbitmq-server
- sudo systemctl enable rabbitmq-server
- sudo systemctl start rabbitmq-server

##### Check the status to make sure everything is running smooth

- sudo systemctl status rabbitmq-server



#### Runnig Everything Smoothly

#### Open Two new Terminal Tab  and activate scripts in your root directory
#### and run these command in each tab

- celery -A mysite worker -l info
- celery -A mysite beat -l info

  To kill previous process if needed

- pkill -9 celery

#### If Everything goes right open Django Admin and open shipments model in Shipment App delete all the previous object and refresh page after 7 secs will sync all shipment in the database.
