import nlp
import unittest

class nlp_test():

  def test_remove_irrelevant_test(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("Baghdad’s ice cream diplomacy | Middle East News | Al Jazeera"),
      "Baghdad’s ice cream diplomacy",
      "Should return: Baghdad’s ice cream diplomacy" )
    self.assertEqual(
      nlp.remove_irrelevant_text("Fact check: Does infrasound from wind farms make people sick? - ABC News"),
      "Fact check: Does infrasound from wind farms make people sick?",
      "Should return: Fact check: Does infrasound from wind farms make people sick?")
    self.assertEqual(
      nlp.remove_irrelevant_text("Bernard Tomic can be helped by Tennis Australia says Davis Cup captain Wally Masur - ABC News"),
      "Bernard Tomic can be helped by Tennis Australia says Davis Cup captain Wally Masur",
      "Should return: Bernard Tomic can be helped by Tennis Australia says Davis Cup captain Wally Masur" )
    self.assertEqual(
      nlp.remove_irrelevant_text("Testing | this out"),
      "this out",
      "Should return: this out" )
    self.assertEqual(
      nlp.remove_irrelevant_text("This is headline | Breaking UK News & World News Headlines"),
      "This is headline",
      "Should return: This is headline" )

class TestSum(unittest.TestCase):

    def test_remove_irrelevant_text(self):
      nlp_test.test_remove_irrelevant_test(self)

unittest.main()
