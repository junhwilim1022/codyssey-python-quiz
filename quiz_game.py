"""콘솔 메뉴, 게임 진행, JSON 저장을 담당한다."""

import json
from pathlib import Path

from quiz import Quiz


STATE_PATH = Path(__file__).resolve().parent / "state.json"


def default_quizzes() -> list[Quiz]:
    """state.json이 없거나 잘못되었을 때 쓸 Python 기초 퀴즈."""
    questions = [
        ("Python에서 화면에 글자를 출력하는 함수는?", ["input()", "print()", "open()", "len()"], 2),
        ("리스트(list)를 만드는 기호는?", ["{}", "()", "[]", "<>"], 3),
        ("조건에 따라 실행할 코드를 나눌 때 쓰는 키워드는?", ["if", "for", "class", "import"], 1),
        ("반복문 중 조건이 참인 동안 실행되는 것은?", ["try", "while", "return", "def"], 2),
        ("JSON 파일을 읽기 위해 사용할 수 있는 표준 모듈은?", ["random", "math", "json", "time"], 3),
        ("함수를 정의할 때 사용하는 키워드는?", ["make", "function", "def", "new"], 3),
    ]
    return [Quiz(question, choices, answer) for question, choices, answer in questions]


class QuizGame:
    def __init__(self, state_path: Path = STATE_PATH):
        self.state_path = Path(state_path)
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.load_state()

    def load_state(self) -> None:
        if not self.state_path.exists():
            print("[안내] 저장 파일이 없어 기본 퀴즈로 시작합니다.")
            self.quizzes = default_quizzes()
            self.best_score = None
            return
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
                raise ValueError("quizzes 목록이 없습니다.")
            score = data.get("best_score")
            if score is not None and (type(score) is not int or not 0 <= score <= 100):
                raise ValueError("best_score 값이 잘못되었습니다.")
            self.quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            self.best_score = score
            print(f"[안내] 저장된 퀴즈 {len(self.quizzes)}개를 불러왔습니다.")
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError) as error:
            print(f"[안내] 저장 파일을 읽지 못했습니다: {error}")
            print("[안내] 기본 퀴즈로 시작합니다. 저장하면 파일이 초기화됩니다.")
            self.quizzes = default_quizzes()
            self.best_score = None

    def save_state(self) -> bool:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with self.state_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            return True
        except (OSError, UnicodeError, TypeError) as error:
            print(f"[오류] 데이터를 저장하지 못했습니다: {error}")
            return False

    @staticmethod
    def read_number(prompt: str, minimum: int, maximum: int) -> int:
        while True:
            value = input(prompt).strip()
            if not value:
                print(f"[안내] 값을 입력해 주세요. ({minimum}~{maximum})")
                continue
            try:
                number = int(value)
            except ValueError:
                print(f"[안내] 숫자를 입력해 주세요. ({minimum}~{maximum})")
                continue
            if minimum <= number <= maximum:
                return number
            print(f"[안내] {minimum}부터 {maximum} 사이의 숫자를 입력해 주세요.")

    @staticmethod
    def read_nonempty(prompt: str) -> str:
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("[안내] 빈 내용은 입력할 수 없습니다.")

    def play(self) -> None:
        if not self.quizzes:
            print("[안내] 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        correct = 0
        total = len(self.quizzes)
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)")
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n--- 문제 {index}/{total} ---")
            quiz.show()
            selected = self.read_number("정답 번호 (1~4): ", 1, 4)
            if quiz.check_answer(selected):
                print("정답입니다!")
                correct += 1
            else:
                print(f"오답입니다. 정답: {quiz.answer}번")
        score = round(correct * 100 / total)
        print(f"\n결과: {total}문제 중 {correct}문제 정답 / {score}점")
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")
        self.save_state()

    def add_quiz(self) -> None:
        print("\n새 퀴즈를 추가합니다.")
        question = self.read_nonempty("문제: ")
        choices = [self.read_nonempty(f"선택지 {number}: ") for number in range(1, 5)]
        answer = self.read_number("정답 번호 (1~4): ", 1, 4)
        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        if self.save_state():
            print("퀴즈를 추가하고 저장했습니다!")
        else:
            print("퀴즈는 현재 실행 중에만 추가되었습니다. 저장 실패를 확인해 주세요.")

    def show_quizzes(self) -> None:
        print(f"\n등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    def show_score(self) -> None:
        if self.best_score is None:
            print("\n아직 퀴즈를 푼 기록이 없습니다.")
        else:
            print(f"\n최고 점수: {self.best_score}점 (100점 만점)")

    def run(self) -> None:
        try:
            while True:
                print("\n" + "=" * 38)
                print("         Python 기초 퀴즈 게임")
                print("=" * 38)
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가")
                print("3. 퀴즈 목록")
                print("4. 점수 확인")
                print("5. 종료")
                print("=" * 38)
                selected = self.read_number("메뉴 선택 (1~5): ", 1, 5)
                if selected == 1:
                    self.play()
                elif selected == 2:
                    self.add_quiz()
                elif selected == 3:
                    self.show_quizzes()
                elif selected == 4:
                    self.show_score()
                else:
                    print("프로그램을 종료합니다.")
                    break
        except (KeyboardInterrupt, EOFError):
            print("\n[안내] 입력이 중단되어 안전하게 종료합니다.")
        finally:
            self.save_state()
