import unittest
import csv
import os
from pandas import RangeIndex
import pandas as pd
import uuid

from pandas_reader.fixtures.fakes import table, DummyModel
from pandas_reader.model import Model, Field
from pandas_reader.manager import Manager
from pandas_reader.setup import config

test_file = os.path.join(config.PACKAGE_DIR, 'fixtures/test.csv')


class ManagerTests(unittest.TestCase):
    """
    There is a bunch of steps to pre-processing DataFrame data structure

    - Remove columns that is not matched
    - Replace column name
    - Add index if model has index_field
    - Replace value
    - Filter rows
    """
    def setUp(self):
        with open(test_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')
            writer.writerows(table)
    
    def tearDown(self):
        os.remove(test_file)

    def test_unmatched_column_removed(self):
        class _Dummy(Model):
            name = Field("학부_과(전공)명", change=lambda x: "_" + x)
            univ = Field("학교명")

        model = _Dummy()
        df = pd.read_csv(test_file)

        manager = Manager(model, df)

        manager.steps[0]()
        self.assertEqual(len(manager.get().columns), 2)

    def test_replace_column_name(self):
        model = DummyModel()
        df = pd.read_csv(test_file)

        manager = Manager(model, df)

        manager.steps[0]()
        manager.steps[1]()
        self.assertEqual(manager.get().columns.tolist(), model.get_colnames())
    
    def test_set_index(self):
        class _Dummy(Model):
            id = Field(index=True)
            name = Field("학부_과(전공)명", change=lambda x: "_" + x)
            univ = Field("학교명")
            college = Field("단과대학명")
            investigation_year = Field("조사년도")

        df = pd.read_csv(test_file)
        default_index = RangeIndex(0, 5, 1)
        for i in default_index:
            self.assertEqual(df.index.to_list()[i], i)

        model = _Dummy()
        manager = Manager(model, df)

        manager.steps[2]()

        for i in range(len(df)):
            self.assertEqual(df.index.to_list()[i], i+1)

        class _Dummy(Model):
            id = Field(index=True, generator=uuid.uuid4)
            name = Field("학부_과(전공)명", change=lambda x: "_" + x)
            univ = Field("학교명")
            college = Field("단과대학명")
            investigation_year = Field("조사년도")
        
        model = _Dummy()
        manager = Manager(model, df)
        
        manager.steps[2]()

        for i in range(len(df)):
            self.assertTrue(isinstance(df.index.to_list()[i], uuid.UUID))
    
    def test_replace_value(self):
        model = DummyModel()
        df = pd.read_csv(test_file)

        manager = Manager(model, df)
        manager.steps[0]()
        manager.steps[1]()
        manager.steps[2]()
        manager.steps[3]()

        is_valid = True
        for i in manager.get()["name"]:
            if not i.startswith("_"):
                is_valid = False
                break
        self.assertTrue(is_valid)


    def test_filter_rows(self):
        model = DummyModel()
        df = pd.read_csv(test_file)

        manager = Manager(model, df)
        manager.steps[0]()
        manager.steps[1]()
        manager.steps[2]()
        manager.steps[3]()
        manager.steps[4]()

        self.assertEqual(len(manager.get()), 2)
