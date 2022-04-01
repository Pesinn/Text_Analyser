import nlp
import unittest
import utils

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
    self.assertEqual(
      nlp.remove_irrelevant_text("This is the article headline | some text | some text | some other text to del"),
      "This is the article headline",
      "Should return: This is the article headline" )

class utils_test():
  def test_remove_duplicate_words(self):
    self.assertEqual(
      utils.remove_duplicate_words("abraham superman is superman but superman is not necessarily abraham"),
      "abraham superman is but not necessarily",
      "Should return: abraham superman is but not necessarily"
    )
    self.assertEqual(
      utils.remove_duplicate_words("this should be returned as it is"),
      "this should be returned as it is",
      "Should return: this should be returned as it is"
    )

  def test_combine_dictionaries(self):
    self.assertEqual(
      utils.combine_dictionaries({
        "19": "CARDINAL",
        "New York": "GPE"
      }, {
        "Queensland": "GPE",
        "New York": "GPE"
      }),
      {
        "19": "CARDINAL",
        "New York": "GPE",
        "Queensland": "GPE"
      },
      """
      Should return: {
        "19": "CARDINAL",
        "New York": "GPE",
        "Queensland": "GPE"
      }
      """
    )

    self.assertEqual(
      utils.combine_dictionaries({
        "11": "CARDINAL",
        "two": "CARDINAL"
      }, {
        "4pm": "TIME",
        "victoria": "GPE"
      }),
      {
        "11": "CARDINAL",
        "two": "CARDINAL",
        "4pm": "TIME",
        "victoria": "GPE"
      },
      """
      Should return: {
        "11": "CARDINAL",
        "two": "CARDINAL",
        "4pm": "TIME",
        "victoria": "GPE"
      }
      """
    )

class TestSum(unittest.TestCase):
    def test_remove_irrelevant_text(self):
      nlp_test.test_remove_irrelevant_test(self)

    def test_remove_duplicate_words(self):
      utils_test.test_remove_duplicate_words(self)

    def test_combine_dictionaries(self):
      utils_test.test_combine_dictionaries(self)

unittest.main()
