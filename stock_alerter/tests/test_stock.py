import unittest
from datetime import datetime
from ..stock import Stock
from ..rule import PriceRule


class StockTest(unittest.TestCase):

    def setUp(self):
        self.goog = Stock('GOOG')
    
    def test_price_of_a_stock_class_should_be_None(self):
        self.assertIsNone(self.goog.price)

    def test_stock_update(self):
        """An update shout set the price on the stock object
        We will be using the `datetime` module for timestamp
        """

        self.goog.update(datetime(2014, 2, 12), price=10)
        self.assertEqual(10, self.goog.price)

    def test_negative_price_shout_throw_ValueError(self):
        with self.assertRaises(ValueError): 
            self.goog.update(datetime(2014, 2, 13), -1)

    def test_stock_price_should_give_the_latest_price(self):
        self.goog.update(datetime(2014, 2, 12), price=10)
        self.goog.update(datetime(2014, 2, 13), price=8.4)
        self.assertAlmostEqual(8.4, self.goog.price, delta=0.0001)

    def given_a_series_of_prices(self, prices):
        timestamps = [datetime(2014, 2, 11), datetime(2014, 2, 12), datetime(2014, 2, 13)]
        for timestamp, price in zip(timestamps, prices):
            self.goog.update(timestamp, price)

    def test_increasing_trend_is_true_if_price_increase_for_3_updates(self):
        self.given_a_series_of_prices([8, 10, 12])
        self.assertTrue(self.goog.is_increasing_trend())
        

    def test_increasting_trend_is_false_if_price_decreas(self):
        self.given_a_series_of_prices([12, 10, 8])
        self.assertFalse(self.goog.is_increasing_trend())

    def test_increasing_trend_is_false_if_price_equal(self):
        self.given_a_series_of_prices([8, 10, 10])
        self.assertFalse(self.goog.is_increasing_trend())


class PriceRuleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        goog = Stock('GOOG')
        goog.update(datetime(2014, 2, 10), 11)
        cls.exchange = {'GOOG': goog}

    def test_a_PriceRule_matches_when_it_meets_the_condition(self):
        rule = PriceRule('GOOG', lambda stock: stock.price > 10)
        self.assertTrue(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_the_condtion_is_not_met(self):
        rule = PriceRule('GOOG', lambda stock: stock.price < 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_priceRule_is_False_if_the_stock_is_not_in_the_exchange(self):        
        rule = PriceRule('MSFT', lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))

    def test_a_PriceRule_is_False_if_the_stock_hasnt_got_an_update_yet(self):
        self.exchange['APPL'] = Stock('APPL')
        rule = PriceRule('APPL', lambda stock: stock.price > 10)
        self.assertFalse(rule.matches(self.exchange))
        
    def test_a_PricesRule_only_depends_on_its_stock(self):
        rule = PriceRule('MSFT', lambda stock: stock.price > 10)
        self.assertEqual({'MSFT'}, rule.depends_on())

