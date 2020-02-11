

### AIRFLOW
![](./img/airflow.png)

#### workflow 관리를 위해 사용 

***DAG : Directed Acyclic Graph <br>
Operator<br>
task***

**DAG**
- 하나의 워크플로우라고 보면 된다. 머신러닝이라는 DAG를 정의한다면
전처리, 학습 , 예측 등이 하나의 DAG가 된다. 

**Operator and task**
- Operator 와 Task의 개념을 알아야하는데 DAG안에 
Operator 함수가 정의되어서 호출되면 task 말이 조금 어렵지만 간단하게 Operator 가 class 라면 그것을 호출해서 사용하는 task 가 곧 Object가 라고 볼 수있다.


**설치**
- ubuntu 서버를 (ec2) 처음 실행 기준 
- airflow 1.10 version 까지 Python2 호환 
- airflow web을 담당하는 flask가 업데이트 되어 airflow 1.10 전까진 호환 x 
- python3 , ubuntu 18.04로 진행 


~~~ 
$ sudo apt-get update
$ sudo apt-get install python3-pip -y
$ sudo pip3 install --upgrade pip3
$ sudo apt-get install python3-setuptools -y
$ sudo apt-get install python3-dev -y
$ sudo apt-get install python3-mysqldb -y
~~~


- airflow 에는 기본 재장 DB에는 SQLite 가 되어있는데 변경 가능하다.postgresql 을 사용하기 위해서 설치작업을 해줌.

~~~

$ sudo apt-get install postgresql postgresql-contrib -y

~~~


이후 postgre로 접속하여 설정해줌 <br>
이름은 Minwoo  DB 명 Airflow 
Minwoo 가 아니라 user 명과 동일하게 해야할듯 

![](./img/root.png) 이 경우엔 Minwoo 대신 root <br>
*root 는 안쓰는게 좋음*

~~~   
    $ sudo -u postgres psql
    
    create role ubuntu;
    create database airflow;
    grant all privileges on database airflow to ubuntu;
    alter role ubuntu superuser;
    alter role ubuntu createdb;
    alter role ubuntu with login;
    grant all privileges on all tables in schema public to ubuntu;
    
    \c airflow
    --> DB 연결 커맨드 
    
    \conninfo
    \q
~~~

의존성이 있는 패키지 미리 설치
```
$ sudo apt-get install libmysqlclient-dev -y
$ sudo apt-get install libssl-dev -y
$ sudo apt-get install libkrb5-dev -y
$ sudo apt-get install libsasl2-dev -y
$ sudo apt-get install libpq-dev

```

*그 다음 airflow 를 설치하게 되는데 그냥 
<br>sudo pip install apache-airflow==1.10.0 <br>하면 에러가 나타남
<br>sudo SLUGIFY_USES_TEXT_UNIDECODE=yes pip install apache-airflow==1.10.0 <br>이런식으로 설치해야함*


**내부에서는 기본 Executor 로 진행됨 그니까 job을 실행주는 느낌
하지만 단일 처리 밖에 못하는 단점이 있음 그렇기 떄문에 병렬 실행이 가능한 Celery 설치 및 관련 패키지 설치**

```
$ sudo pip3 install celery
$ sudo apt-get install libpcap-dev libpq-dev
$ sudo pip3 install psycopg2
$ sudo pip3 install mysqlclient
$ sudo pip3 install psycopg2-binary
$ sudo pip3 install apache-airflow['kubernetes']
$ sudo pip3 install apache-airflow[celery]
$ sudo pip3 install apache-airflow[rabbitmq]
$ sudo pip3 install apache-airflow[mysql]
$ sudo pip3 install apache-airflow[postgres]

```

celey 를 설치한 후엔 RabbitMQ 를 설치하여 Message Broker로 사용<br>
![](./img/rabbit.png)


[psycopg2 에러 참고](https://github.com/facebook/prophet/issues/418)

rabbitmq 가 정상적으로 설치가 된다면 quest 계정이 자동으로 설치됨

설치 및 구성 
```
sudo apt install rabbitmq-server -y

sudo vi /etc/rabbitmq/rabbitmq-env.conf
# 아래 설정 추가
NODE_IP_ADDRESS=0.0.0.0
```

*만약 $username role error 같은게 발생하면 저 NODE_IP_ADDRESS 확인 해볼 것 아니면 airflow 폴더 삭제하고 airflow init 다시 진행 후 설정 다시 해보거나 그것도 아니면 현재 sudo 명령어 말고 그냥 psql 해서 들어가지나 확인 이 셋중에 해결되는 방법이 있음 그냥 psql 하려면 아래 코드 실행해서 변경해주면 가능 아래 코드는 안해도 될 듯 이건 보류 위에서 root 로 맞춰줬으니까*


```
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
```

rabbitmq 실행

``` sudo service rabbitmq-server start```

필요한 것들 설치 되면 airflow 초기화


```airflow initdb```

airflow 설정 파일 변경해야함 




아래 코드가 된다면 무방하나 rabbimq 버전에서 지원 안할 가능성 농후

~vi airflow/airflow.cfg~ 

~executor = CeleryExecutor~
~sql_alchemy_conn = postgresql+psycopg2:///airflow~
~broker_url = amqp://guest:guest@localhost:5672//~
~result_backend = amqp://guest:guest@localhost:5672//~


이 방법으로 수정 
amqp 가 아니라 pyamqp로 진행
result_backend 도 postgre 를 지정 

``` 

sudo pip3 install pyamqp

vi airflow/airflow.cfg 

executor = CeleryExecutor
sql_alchemy_conn = postgresql+psycopg2:///airflow
broker_url = pyamqp://guest:guest@localhost:5672//
result_backend = db+postgresql://airflow:airflow@postgres/airflow
```

![단어](./img/word.png)

기본적으로 게스트 계정 생성됨 위에 브로커 url 하고 result_backend 는 동일한 값으로 설정하거나 result_backend 를 sql_alchemy_conn 이랑 맞춰줄 수 있음 아니면 rabbitmq 계정을 생성해서 guest 대신 쓸 수 있음


설정 해준 후 다시 initdb 명령으로 초기화



dag를 담을 폴더 생성 
``` mkdir -p ~/airflow/dags ```

다 됬으면 이제 실행합니다. 

```
$ airflow scheduler -D
$ airflow worker -D
$ airflow webserver -p 8080 -D
```

정상 실행 된다면  8080 포트 번호로 들어 갈 수 있습니다.

**만약 인바운드 설정을 안해줬더면 들어갈 수 없으니 aws 경우 인바운드 설정을 해줘야 합니다.**


**만약 OSError: [Errno 2] No such file or directory 이 error 가 발생한다면 파이썬 PATH 문제입니다.**
- 이 경우 확인 할 것 
    - 1. which python 을 통해 파이썬이 어디에 깔려 있는지 확인
    - 2. vi ~/.bash_proffile 에 환경변수 적용 여부 확인(아마 안되있을 것)
    - 3. 아래 첨부 코드 처럼 추가 <br>
    
    ```
    PATH=$PATH:$HOME/bin

    export PATH
    export PATH=/usr/local/bin:~/.local/bin:$PATH

    ```
    - 4. source ~/.bash_profile
    
**Celery Executor을 사용한다면 worker를 동작시켜야하고 동작 되는지 확인해야함. queued 나 scheduled되있는데 run을 안한다면 worker 동작 안하고 있을 가능성 큼**




  
   
참고 사이트 

[우분투에 AIRFLOW 설치하기](https://jungwoon.github.io/airflow/2019/02/26/Airflow/)<br>
[Airflow 설치](http://sanghun.xyz/2017/12/airflow-4.-celeryexecutor-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0/)<br>
[GCP에 AIRFLOW 설치하기](https://yamerong.tistory.com/52)<br>
[RabbitMQ](http://sanghun.xyz/2017/12/airflow-4.-celeryexecutor-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0/)<br>
[psycopg2 error](https://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi)<br>
[RabbitMq airflow](https://vujade.co/install-apache-airflow-ubuntu-18-04/)<br>
[Airflow tasks get stuck at “queued” status and never gets running](https://stackoverflow.com/questions/45853013/airflow-tasks-get-stuck-at-queued-status-and-never-gets-running)<br>
[doc](http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html)





