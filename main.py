from quiz_game import QuizGame


def main():
    game = QuizGame()

    while True:
        try:
            print("\n===== 코디세이 퀴즈 게임 =====")
            print("1. 퀴즈 풀기")
            print("2. 문제 추가")
            print("3. 문제 목록")
            print("4. 점수 확인")
            print("5. 종료")
            print("메뉴 번호 1~5를 입력하세요.")
            choice = input("메뉴 선택: ").strip()

            if choice == "1":
                game.play()
            elif choice == "2":
                game.add_quiz()
            elif choice == "3":
                game.show_quizzes()
            elif choice == "4":
                game.show_score()
            elif choice == "5":
                print("게임을 종료합니다.")
                break
            else:
                print("잘못 입력했습니다. 1~5 중에서 선택하세요.")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C나 입력 종료가 발생해도 점수는 저장합니다.
            print("\n입력이 중단되어 게임을 종료합니다.")
            game.save()
            break


if __name__ == "__main__":
    main()
