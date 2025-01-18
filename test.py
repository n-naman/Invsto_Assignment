import unittest
import pandas as pd
from moving_average_strategy import moving_average_strategy as calculate_signals  # Import your signal calculation function

class TestMovingAverageStrategy(unittest.TestCase):
    def setUp(self):
        # Sample data
        self.data = pd.DataFrame({
            'datetime': pd.date_range(start='2023-01-01', periods=10, freq='D'),
            'close': [100, 102, 101, 105, 107, 106, 110, 111, 115, 117]
        })

    def test_calculate_signals(self):
        # Test if signals are calculated without errors
        self.data = calculate_signals(self.data, short_window=3, long_window=5)
        self.assertTrue('Signal' in self.data.columns)
        self.assertTrue(self.data['Signal'].notnull().all())

    def test_data_types(self):
        # Validate column data types
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.data['datetime']))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.data['close']))

if __name__ == '__main__':
    unittest.main()
