

### AIRFLOW
![](./img/airflow.PNG)

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

~~~ 
$ sudo apt-get update
$ sudo apt-get install python-pip -y
$ sudo pip install --upgrade pip
$ sudo apt-get install python-setuptools -y
$ sudo apt-get install python-dev -y
$ sudo apt-get install python-mysqldb -y
~~~


- airflow 에는 기본 재장 DB에는 SQLite 가 되어있는데 변경 가능하다.postgresql 을 사용하기 위해서 설치작업을 해줌.

~~~

$ sudo apt-get install postgresql postgresql-contrib -y

~~~


이후 postgre로 접속하여 설정해줌 <br>
이름은 Minwoo  DB 명 Airflow 
~~~   
    $ sudo -u postgres psql
    
    create role Minwoo;
    create database airflow;
    grant all privileges on database airflow to Minwoo;
    alter role Minwoo superuser;
    alter role Minwoo createdb;
    alter role Minwoo with login;
    grant all privileges on all tables in schema public to Minwoo;
    
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
$ sudo pip install celery
$ sudo pip install psycopg2
$ sudo pip install mysqlclient
$ sudo pip install psycopg2-binary
$ sudo pip install apache-airflow['kubernetes']
$ sudo pip install apache-airflow[celery]
$ sudo pip install apache-airflow[rabbitmq]
$ sudo pip install apache-airflow[mysql]
$ sudo pip install apache-airflow[postgres]

```

celey 를 설치한 후엔 RabbitMQ 를 설치하여 Message Broker로 사용<br>
![](./img/rabbit.PNG)

설치 및 구성 
```
sudo apt install rabbitmq-server -y

sudo vi /etc/rabbitmq/rabbitmq-env.conf
# 아래 설정 추가
NODE_IP_ADDRESS=0.0.0.0
```

*만약 $username role error 같은게 발생하면 저 NODE_IP_ADDRESS 확인 해볼 것 아니면 airflow 폴더 삭제하고 airflow init 다시 진행 후 설정 다시 해보거나 그것도 아니면 현재 sudo 명령어 말고 그냥 psql 해서 들어가지나 확인 이 셋중에 해결되는 방법이 있음 그냥 psql 하려면 아래 코드 실행해서 변경해주면 가능

```
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
```

rabbitmq 실행

``` sudo service rabbitmq-server start```

필요한 것들 설치 되면 airflow 초기화


```airflow initdb```

airflow 설정 파일 변경해야함 

``` 
vi airflow/airflow.cfg 

executor = CeleryExecutor
sql_alchemy_conn = postgresql+psycopg2:///airflow
broker_url = amqp://guest:guest@localhost:5672//
result_backend = amqp://guest:guest@localhost:5672//
```

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

** 만약 인바운드 설정을 안해줬더면 들어갈 수 없으니 aws 경우 인바운드 설정을 해줘야 합니다.* *


** 만약 OSError: [Errno 2] No such file or directory 이 error 가 발생한다면 파이썬 PATH 문제입니다.* *
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
    
    
    

