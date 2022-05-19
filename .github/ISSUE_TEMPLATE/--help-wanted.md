---
name: "\U0001F44BHelp wanted"
about: 어떤 도움이 필요한가요?
title: ''
labels: help wanted
assignees: ''

---

### ✔ 기존에 어떻게 했는지?
- git에 push 할 때 각자 작성한 코드를 push함 



###  ✔ 도움이 필요한 부분
- 팀 전체 코드의 통일성을 위해서 pre-commit을 적용할 필요가 있을것 같아서 필요한 내용들을 찾아봤습니다.

**적용방법**
1. pip install pre-commit (**mac** : brew install pre-commit  )  #설치
2. pre-commit sample-config > .pre-commit-config.yaml  #파일생성 : 아래처럼 4개의 훅(id) 생성

```
# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.2.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```
 

- 추가가 필요한 hook 논의가 필요할듯하며 일단, 기본적인 4개만 세팅

3. pre-commit install  #자동으로 커밋할때 검사 수행하도록 설치
4. git add {추가할 파일}
5. git commit #검사후 수정이 필요할 경우 자동으로 수정됨
6. git add {수정된 추가할 파일}
7. git commit #커밋 메시지 작성(기존 방법대로)
8. git push



### ✔ 참고한(할) 링크 추가
[프리커밋 적용방법](https://www.daleseo.com/pre-commit/)



### ✔ 고민한 시간
