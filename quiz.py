class Quiz:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer(self, user_answer):
        # 공백과 대소문자 차이를 무시합니다.
        return user_answer.strip().lower() == self.answer.strip().lower()
