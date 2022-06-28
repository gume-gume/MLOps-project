## :rocket: What is MLOps?
MLOps는 DevOps의 목표와 마찬가지로 사용자에게 서비스를 빠르게 전달하는 개발 문화입니다.
DevOps에서는 “코드 통합, 테스트, 배포, 테스트, 모니터링” 의 파이프라인을 자동화하여 이 목표를 달성합니다.
MLOps는 DevOps에 ML이 추가된 것입니다.

## :bell: Purpose

- 머신러닝의 학습, 배포, 저장 자동화 라인 구현.
- 데이터 사이언티스트와 소프트웨어 엔지니어에게 협업 환경을 제공

## 💾 Data
- Income Dataset
- Perform Binary Classification to predict if Salary is greater than $50K

## 📚 Tech Stacks
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python3.9.7](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
<div align=left>
    <img src="https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white">
    <img src="https://img.shields.io/badge/Minio-569A31?style=for-the-badge&logo=Amazon S3&logoColor=ffdd54">
    <img src="https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache Airflow&logoColor=white">
    <img src ="https://img.shields.io/badge/Git Action-2088FF?style=for-the-badge&logo=GitHub Actions&logoColor=white">
    <br>

## 🎬 Phase 0 (2022.05.01 - 2022.05.22)

### Phase 0 흐름도
<img width="814" alt="image" src="https://user-images.githubusercontent.com/70750888/176097551-7646697e-e33e-46e1-9c44-a288f928d7ea.png">


### 1. 개발환경 세팅
- git-flow : github flow 채택
- github에서 사용할 issue와 pr 템플릿 생성
- pre-commit을 통한 code 스타일 통일
- python 3.9.7
- gcp를 통해서 unbuntu20.04 서버생성(ssh접속)

### 2. 머신러닝 파이프라인 구축
- load_model, preprocessing, labeling 등등의 함수 작성
- issue : joblib라이브러리를 통해서 로컬에 있는 큰 사이즈의 model을 바로 서버에서 로드할 경우 속도 문제 발생

### 3. PostgreSQL & Docker를 활용한 데이터베이스 구현
- docker를 통해서 postgreSQL 데이터베이스 세팅
- postgreSQL에 데이터 적재

### 4. FastAPI를 활용한 Rest API 서버 구현
- reidsai를 통한 model serving
- exception 정의 및 handler 작성

#### Tree 구조

```bash
app
├── main.py
├── config.py
├── db
│   ├── database.py
│   └── models.py
├── routers
│   └── income.py
├── schemas
│   ├── request.py
│   └── response.py
├── service
│   └── app_service.py
└── utils
    ├── app_exceptions.py
    ├── handlers.py
    ├── request_exceptions.py
    └── service_result.py
```

## 🎬 Phase 1 (2022.05.23 - 2022.06.28)

### Phase 1 흐름도

<img width="801" alt="스크린샷 2022-06-28 오후 12 57 21" src="https://user-images.githubusercontent.com/70750888/176097624-3413beb5-6c67-4c1e-9fd8-a7da0eeee20a.png">

### 0. 데이터 변경
- Income 데이터의 경우 csv 파일이라 제한적임
- 실시간 데이터 수집을 위해 Income Dataset -> Upbit의 BTC, ETH, ADA 코인 수집

### 1. Mlflow & Minio를 활용한 실험관리, 모델관리
- Mlflow를 이용하여 실험관리, 모델관리
- Minio를 이용한 모델 저장 스토리지로 사용

### 2. 지속적 통합/ 지속적 배포
- GitHub Actions과 Docker Compose를 이용하여 CI CD 실현
- 모델을 더 빠른 주기로 서빙하면서도 신뢰도 및 정확도를 유지하는 것을 목표

#### CI CD 구조
<img width="781" alt="스크린샷 2022-06-28 오후 2 23 12" src="https://user-images.githubusercontent.com/70750888/176099176-d4c2da39-ed02-43bd-93c3-92bb48d68dde.png">



### 3. 지속적 훈련
- Airflow를 활용하여 BTC, ETH, ADA 4시간 간격으로 데이터 수집과 검증 자동화
- Airflow를 활용하여 수집된 데이터 자동 훈련


#### Tree 구조
```bash
main.py
app
├── config.py
├── db
│   ├── database.py
│   └── models.py
├── routers
│   └── income.py
├── schemas
│   ├── request.py
│   └── response.py
├── service
│   └── app_service.py
├── utils
│   ├── app_exceptions.py
│   ├── handlers.py
│   ├── request_exceptions.py
│   └── service_result.py
coin
├──coin_preict.py
├──coin_service.py
├──data_collection.py
├──data_verification.py
├──utiles.py
├──config.py
dags
├──btc_flow.py
├──eth_flow.py
└──ada_flow.py
```
