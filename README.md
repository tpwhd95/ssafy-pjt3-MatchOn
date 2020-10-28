# 매치ON

## 1. 패키지 설치
### 1-1. backend
#### 가상환경 설정
```bash
$ python -m venv venv
# 가상환경은 git 레퍼지토리에 기록되지 않으므로 각자 설정해주어야 합니다.
```
#### 가상환경 켜기
```bash
# ven가 위치하는 폴더에서
$ source venv/Scripts/activate
```
#### 가상환경 그기
```bash
$ deactivate
```

#### pip 리스트 갱신
```bash
$ pip freeze > requirements.txt
```
#### pip 설치
```bash
$ pip install -r requirements.txt
```
#### 1-2. frontend
```bash
$ npm i
# npm-shrinkwrap.json에 기록된 라이브러리가 자동으로 설치됩니다.
```

### 2. Commit 그라운드 룰
#### 커밋 메시지
```bash
$ git commit -m "S03P31A306-29 | Backend Devtools Setup Done"
# 지라 이슈번호 | 커밋메시지로 적습니다.
```

#### feature 관리
```bash
$ git branch(혹은 checkout) feature/user-accounts-setup
# feature/기능이름으로 적습니다.
# 해당 브랜치는 develop으로 병합 후 삭제합니다.
```