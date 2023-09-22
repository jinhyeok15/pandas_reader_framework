import unittest
import pandas as pd
import os
import csv

from pandas_reader.fixtures.fakes import table, in_mem_csv
from pandas_reader.setup import config

test_file = os.path.join(config.PACKAGE_DIR, 'fixtures/test.csv')


class PandasTests(unittest.TestCase):
    def setUp(self):
        with open(test_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')
            writer.writerows(table)

    def tearDown(self):
        os.remove(test_file)

    def test_different_source_extension(self):
        """
        If you config different file type from the source,
        you get error like this.
        """
        self.assertRaises(ValueError, lambda: pd.read_excel(in_mem_csv))

    def test_read_xx_can_use_relpath(self):
        """
        It is safe using relative path when you implement pre_processing
        """
        pd.read_csv(test_file)
        self.assertRaises(FileNotFoundError, lambda: pd.read_csv(test_file + "1"))
