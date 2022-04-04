from datetime import date

import nlp
import unittest
import utils

class nlp_remove_irrelevant_text():
  def three_stubs_two_last_irrelevant(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("Baghdad’s ice cream diplomacy | Middle East News | Al Jazeera"),
      "Baghdad’s ice cream diplomacy",
      "Should return: Baghdad’s ice cream diplomacy")
    
  def text_with_colon_last_irrelevant(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("Fact check: Does infrasound from wind farms make people sick? - ABC News"),
      "Fact check: Does infrasound from wind farms make people sick?",
      "Should return: Fact check: Does infrasound from wind farms make people sick?")
    
  def two_stubs_last_irrelevant(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("Bernard Tomic can be helped by Tennis Australia says Davis Cup captain Wally Masur - ABC News"),
      "Bernard Tomic can be helped by Tennis Australia says Davis Cup captain Wally Masur",
      "Should return: Bernard Tomic can be helped by Tennis Australia says Davis Cup captain Wally Masur" )

  def two_stubs_first_irrelevant(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("Testing | this out"),
      "this out",
      "Should return: this out" )

  def two_stubs_last_part_of_igonre_array(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("This is headline | Breaking UK News & World News Headlines"),
      "This is headline",
      "Should return: This is headline" )

  def four_stubs_drop_three_last(self):
    self.assertEqual(
      nlp.remove_irrelevant_text("This is the article headline | some text | some text | some other text to del"),
      "This is the article headline",
      "Should return: This is the article headline" )

class utils_remove_duplicate_words():
  def a_lot_of_duplicates_all_over(self):
    self.assertEqual(
      utils.remove_duplicate_words("abraham superman is superman but superman is not necessarily abraham"),
      "abraham superman is but not necessarily",
      "Should return: abraham superman is but not necessarily"
    )
  def no_duplicates(self):
    self.assertEqual(
      utils.remove_duplicate_words("this should be returned as it is"),
      "this should be returned as it is",
      "Should return: this should be returned as it is"
    )

class utils_combine_dictionaries:
  def last_item_identical(self):
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

  def no_item_identical(self):
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

class utils_convert_to_datetime:  
  def valid_date(self):
    self.assertEqual(utils.convert_to_datetime("20210512"), date(2021, 5, 12), "Date should be: 2021, 5, 12")
  def only_year_date(self):
    self.assertEqual(utils.convert_to_datetime("2020"), date(2020, 1, 1), "Date should be: 2020, 1, 1")
  def invalid_date(self):
    with self.assertRaises(Exception):
      utils.convert_to_datetime("sometext")
  def too_many_digits(self):
    with self.assertRaises(Exception):
      utils.convert_to_datetime("20200911811401101")

class NLP_Test(unittest.TestCase):
  def test_remove_irrelevant_text(self):
    nlp_remove_irrelevant_text.three_stubs_two_last_irrelevant(self)
    nlp_remove_irrelevant_text.text_with_colon_last_irrelevant(self)
    nlp_remove_irrelevant_text.two_stubs_last_irrelevant(self)
    nlp_remove_irrelevant_text.two_stubs_first_irrelevant(self)
    nlp_remove_irrelevant_text.two_stubs_last_part_of_igonre_array(self)
    nlp_remove_irrelevant_text.four_stubs_drop_three_last(self)

class Utils_Test(unittest.TestCase):
  def test_remove_duplicate_words(self):
    utils_remove_duplicate_words.a_lot_of_duplicates_all_over(self)
    utils_remove_duplicate_words.no_duplicates(self)

  def test_combine_dictionaries(self):
    utils_combine_dictionaries.last_item_identical(self)
    utils_combine_dictionaries.no_item_identical(self)
    
  def test_convert_to_datetime(self):
    utils_convert_to_datetime.valid_date(self)
    utils_convert_to_datetime.only_year_date(self)
    utils_convert_to_datetime.invalid_date(self)
    utils_convert_to_datetime.too_many_digits(self)

unittest.main()
