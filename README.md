# Hi! We are gume-gume

이대형, 장영동, 정선규

# :rocket: What is MLOps?

MLOps는 DevOps의 목표와 마찬가지로 사용자에게 서비스를 빠르게 전달하는 개발 문화입니다. 
DevOps에서는 “코드 통합, 테스트, 배포, 테스트, 모니터링” 의 파이프라인을 자동화하여 이 목표를 달성합니다.
MLOps는 DevOps에 ML이 추가된 것입니다.

# :bell: Purpose

- 머신러닝의 학습, 배포, 저장 자동화 라인 구현.
- 데이터 사이언티스트와 소프트웨어 엔지니어에게 협업 환경을 제공

# Phase 0 (2022.05.01 - 2022.05.22)

- Postgresql local DB 생성 
  - Phase 1에서 GCP에 연동할 예정
  - why? 각 개인의 노트북에 postgresql 아이디, 비밀번호가 다를수도 있기에 공동의 DB만들기
- Mlflow로 모델 서빙
- Minio 연동하여 스토리지 생성
- 모델 예측 및 학습 구현


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
