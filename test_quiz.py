import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from quiz import Quiz
from quiz_game import QuizGame


class QuizTests(unittest.TestCase):
    def test_answer(self):
        q = Quiz("출력 함수?", "print")
        self.assertTrue(q.check_answer(" PRINT "))
        self.assertFalse(q.check_answer("input"))

    def test_save_load_best_score(self):
        with tempfile.TemporaryDirectory() as folder:
            game = QuizGame()
            game.file_path = Path(folder) / "state.json"
            game.played = 5
            game.correct = 4
            game.best_score = 4
            game.save()
            other = QuizGame()
            other.file_path = game.file_path
            other.load()
            self.assertEqual(other.best_score, 4)
            self.assertEqual(other.correct, 4)

    def test_backup_and_restore(self):
        with tempfile.TemporaryDirectory() as folder:
            game = QuizGame()
            game.file_path = Path(folder) / "state.json"
            game.save()
            game.played = 5
            game.save()
            self.assertTrue(game.backup_path().exists())
            game.file_path.write_text("{broken", encoding="utf-8")
            other = QuizGame()
            other.file_path = game.file_path
            with patch("builtins.input", return_value="1"):
                other.load()
            self.assertTrue((Path(folder) / "state.broken.json").exists())
            self.assertEqual(other.played, 0)


if __name__ == "__main__":
    unittest.main()
