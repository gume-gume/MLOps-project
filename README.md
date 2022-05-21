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

## Phase 0 (2022.05.01 - 2022.05.22)
![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python3.9.7](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
<!-- ![Mlflow](https://img.shields.io/badge/Mlflow-0.13-green) -->

- Scikit-Learn 베이스의 머신러닝 파이프라인 구현  
- FastAPI를 활용한 Rest API 서버 구현
- PostgreSQL & Docker를 활용한 데이터베이스 구현
- Mlflow 및 Minio를 활용한 모델 레지스트리 구현


```bash
├── DB
│   ├── create_db.py
│   ├── database.py
│   └── models.py
├── errors
│   ├── app_exceptions.py
│   ├── handlers.py
│   ├── request_exceptions.py
│   └── service_result.py
├── routers
│   └── redisai.py
│   
└── schemas
    ├── request.py
    └── response.py
``` 
