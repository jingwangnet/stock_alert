import unittest

class StockTest(unittest.TestCase):
    
    def test_price_of_a_stock_class_should_be_None(self):
        stock = Stock('GOOG')
        self.assertIsNone(stock.price)


if __name__ == '__main__':
    unittest.main()
