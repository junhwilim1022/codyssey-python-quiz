"""퀴즈 한 문제를 표현하는 클래스."""


class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제 내용이 비어 있습니다.")
        if not isinstance(choices, list) or len(choices) != 4 or any(
            not isinstance(choice, str) or not choice.strip() for choice in choices
        ):
            raise ValueError("선택지는 비어 있지 않은 문자열 4개여야 합니다.")
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1부터 4 사이의 정수여야 합니다.")
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def show(self) -> None:
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"  {number}. {choice}")

    def check_answer(self, selected: int) -> bool:
        return selected == self.answer

    def to_dict(self) -> dict:
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터가 올바른 객체가 아닙니다.")
        return cls(data["question"], data["choices"], data["answer"])
