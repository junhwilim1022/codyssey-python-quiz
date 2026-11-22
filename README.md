# 코디세이 미션 2 - Python 퀴즈 게임

파이썬으로 터미널에서 실행하는 퀴즈 게임을 만들었다. 입력, 조건문, 반복문, 클래스, JSON 파일 저장을 연습하는 과제다.

## 실행 방법

PowerShell에서 프로젝트 폴더로 이동한 뒤 다음 명령어를 입력한다.

```powershell
python main.py
```

메뉴는 1번 퀴즈 풀기, 2번 문제 추가, 3번 문제 목록, 4번 점수 확인, 5번 종료로 구성했다. 기본 문제는 5개다. 문제를 추가하면 `state.json`에 저장된다.

## 파일 구성

- `main.py`: 메뉴를 반복해서 보여주고 번호에 따라 기능 실행
- `quiz.py`: `Quiz` 클래스로 문제와 정답 비교
- `quiz_game.py`: `QuizGame` 클래스로 퀴즈 진행, 점수 계산, 파일 저장
- `state.json`: 문제 목록과 점수 저장
- `test_quiz.py`: 정답 비교와 파일 저장 테스트

클래스는 문제 데이터와 기능을 묶으려고 사용했다. 함수만으로 만들 수도 있지만 문제와 게임 기능을 구분하면 수정할 때 파일을 찾기 편하다.

## 저장 방식

`state.json`의 `quizzes`에는 문제와 답이 들어 있고 `played`는 지금까지 푼 문제 수, `correct`는 누적 정답 수다. `best_score`는 한 번 퀴즈를 풀 때 가장 많이 맞힌 문제 수다. 예전 저장 파일에 `best_score`가 없어도 0으로 읽는다.

JSON은 사람이 직접 내용을 확인하기 쉽고 별도 설치가 필요 없어서 선택했다. 대신 문제가 많이 쌓이면 파일 전체를 읽고 쓰기 때문에 효율이 떨어질 수 있다. 데이터가 많아지면 데이터베이스를 사용하는 방법도 있을 것 같다.

저장할 때 기존 파일이 정상적인 JSON이면 `state.backup.json`에 이전 내용을 복사한다. 파일을 읽지 못하면 백업으로 복구하거나 기본 문제로 초기화할 수 있게 했다. 복구 전의 잘못된 파일은 `state.broken.json`으로 남긴다.

## Git과 테스트

Git 커밋은 기능 추가(`feat:`), 오류 수정(`fix:`), 문서 수정(`docs:`)처럼 나누어 기록한다. 기능을 따로 작업할 때 브랜치를 사용하고 main으로 합칠 수 있다. 충돌이 나면 내용을 확인하고 고친 뒤 병합을 계속한다.

```powershell
python -m unittest test_quiz.py
git log --oneline -15
git log --oneline --graph --all
git branch -a
git remote -v
```

실행해 확인할 내용: 기본 문제 5개, 문제 추가 후 재실행, 점수 저장, 최고 점수 갱신, 잘못된 JSON에서 복구 선택, Ctrl+C 종료.

GitHub 저장소: https://github.com/junhwilim1022/codyssey-python-quiz

Git 명령 실행 결과와 스크린샷은 `GIT_SCREENSHOT_GUIDE.md`에 정리한 방법으로 확인할 수 있다. 예시 이력과 직접 실행한 기록은 구분한다.
