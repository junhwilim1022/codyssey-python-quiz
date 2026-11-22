import json
import shutil
from pathlib import Path
from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.file_path = Path(__file__).with_name("state.json")
        self.quizzes = [
            Quiz("파이썬에서 출력할 때 쓰는 함수는?", "print"),
            Quiz("리스트를 감싸는 기호는? (대괄호/소괄호)", "대괄호"),
            Quiz("Git에서 변경 기록을 저장하는 명령어는?", "commit"),
            Quiz("파이썬에서 키보드 입력을 받는 함수는?", "input"),
            Quiz("Git에서 현재 변경 상태를 확인하는 명령어는?", "status"),
        ]
        self.played = 0
        self.correct = 0
        self.best_score = 0
        self.load()

    def play(self):
        print("\n=== 퀴즈 시작 ===")
        round_score = 0
        for quiz in self.quizzes:
            print("\n문제:", quiz.question)
            answer = input("정답: ")
            self.played += 1
            if quiz.check_answer(answer):
                print("정답입니다!")
                self.correct += 1
                round_score += 1
            else:
                print("틀렸습니다. 정답:", quiz.answer)
        print("이번 점수:", round_score, "/", len(self.quizzes))
        if round_score > self.best_score:
            self.best_score = round_score
        print("퀴즈가 끝났습니다.")
        self.save()

    def add_quiz(self):
        question = input("새 문제: ").strip()
        answer = input("새 정답: ").strip()
        if question == "" or answer == "":
            print("문제와 정답을 모두 입력해야 합니다.")
            return
        self.quizzes.append(Quiz(question, answer))
        print("문제를 추가했습니다.")
        self.save()

    def show_quizzes(self):
        print("\n=== 문제 목록 ===")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(str(number) + ". " + quiz.question)

    def show_score(self):
        print("지금까지 맞힌 문제:", self.correct, "/", self.played)
        print("한 번에 가장 많이 맞힌 문제:", self.best_score)

    def save(self):
        data = {
            "quizzes": [],
            "played": self.played,
            "correct": self.correct,
            "best_score": self.best_score,
        }
        for quiz in self.quizzes:
            data["quizzes"].append({"question": quiz.question, "answer": quiz.answer})
        try:
            # 기존 파일이 정상 JSON일 때만 이전 내용을 백업합니다.
            if self.file_path.exists():
                try:
                    with open(self.file_path, "r", encoding="utf-8") as old_file:
                        json.load(old_file)
                    shutil.copy2(self.file_path, self.backup_path())
                except (OSError, UnicodeError, json.JSONDecodeError):
                    pass
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print("파일 저장에 실패했습니다:", error)

    def backup_path(self):
        return self.file_path.with_suffix(".backup.json")

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            quizzes = data["quizzes"]
            played = data["played"]
            correct = data["correct"]
            best_score = data.get("best_score", 0)  # 예전 저장 파일도 읽을 수 있게 합니다.
            if not isinstance(quizzes, list) or not isinstance(played, int) or not isinstance(correct, int) or not isinstance(best_score, int):
                raise ValueError("저장된 데이터 형식이 다릅니다.")
            new_quizzes = []
            for item in quizzes:
                new_quizzes.append(Quiz(item["question"], item["answer"]))
            if not all(isinstance(q.question, str) and isinstance(q.answer, str) for q in new_quizzes):
                raise ValueError("문제 데이터가 문자열이 아닙니다.")
            if played < 0 or correct < 0 or correct > played or best_score < 0:
                raise ValueError("점수 데이터가 올바르지 않습니다.")
            self.quizzes = new_quizzes
            self.played = played
            self.correct = correct
            self.best_score = best_score
        except FileNotFoundError:
            print("저장 파일이 없어 기본 문제로 시작합니다.")
            self.save()
        except (json.JSONDecodeError, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
            print("저장 파일에 문제가 있습니다:", error)
            backup = self.backup_path()
            if backup.exists():
                print("1. 백업 파일로 복구하기")
                print("2. 기본 문제로 다시 시작하기")
                try:
                    choice = input("선택 (1/2): ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("저장 파일은 변경하지 않았습니다.")
                    return
                if choice == "1":
                    try:
                        with open(backup, "r", encoding="utf-8") as file:
                            backup_data = json.load(file)
                        if not isinstance(backup_data.get("quizzes"), list):
                            raise ValueError("백업 문제 목록이 잘못되었습니다.")
                        if not isinstance(backup_data.get("played"), int) or not isinstance(backup_data.get("correct"), int):
                            raise ValueError("백업 점수가 잘못되었습니다.")
                        # 기존 파일은 다른 이름으로 남겨두고 복구합니다.
                        broken = self.file_path.with_suffix(".broken.json")
                        if self.file_path.exists():
                            shutil.copy2(self.file_path, broken)
                        # 복구 파일 구조가 맞는지 load()로 다시 확인합니다.
                        shutil.copy2(backup, self.file_path)
                        self.load()
                        print("백업 파일로 복구했습니다.")
                        return
                    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, AttributeError) as backup_error:
                        print("백업 파일도 읽을 수 없습니다:", backup_error)
            else:
                print("백업 파일이 없습니다.")
            try:
                choice = input("기본 문제로 초기화할까요? (y/n): ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("저장 파일은 변경하지 않았습니다.")
                return
            if choice == "y":
                try:
                    if self.file_path.exists():
                        shutil.copy2(self.file_path, self.file_path.with_suffix(".broken.json"))
                    self.save()
                    print("기본 문제로 초기화했습니다.")
                except OSError as save_error:
                    print("초기화 중 오류가 발생했습니다:", save_error)
            else:
                print("저장 파일은 변경하지 않았습니다.")
