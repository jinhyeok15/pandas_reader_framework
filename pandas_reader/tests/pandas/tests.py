import unittest
import pandas as pd
import os
import csv

from pandas_reader.fixtures.fakes import table, in_mem_csv
from pandas_reader.setup import config

test_csv_file = os.path.join(config.PACKAGE_DIR, 'fixtures/test.csv')
test_excel_file = os.path.join(config.PACKAGE_DIR, 'fixtures/test.xlsx')
test_json_file = os.path.join(config.PACKAGE_DIR, 'fixtures/test.json')


class PandasTests(unittest.TestCase):
    def setUp(self):
        with open(test_csv_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')
            writer.writerows(table)
        
        df = pd.read_csv(test_csv_file)
        with pd.ExcelWriter(test_excel_file) as excel_writer:
            df.to_excel(excel_writer, index=False)
        
        df.to_json(test_json_file)

    def tearDown(self):
        os.remove(test_csv_file)
        os.remove(test_excel_file)
        os.remove(test_json_file)

    def test_different_source_extension(self):
        """
        If you config different file type from the source,
        you get error like this.
        """
        self.assertRaises(ValueError, lambda: pd.read_excel(in_mem_csv))

    def test_io(self):
        """
        Using pandas io api
        """
        pd.read_csv(test_csv_file)
        pd.read_excel(test_excel_file, engine='openpyxl')
        pd.read_json(test_json_file)
