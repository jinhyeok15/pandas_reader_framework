import unittest
from unittest import mock
import pandas as pd
from pandas import RangeIndex
import os
import csv
import inspect
import uuid

from fixtures.fakes import *
from manager import Manager

test_file = './fixtures/test.csv'


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


class ModelTests(unittest.TestCase):
    """
    Manager uses Model to change columns and values by checking the Field element.
    So you need to check model instance properties.

    1. meta
    - Model information should follow the declaration

    2. get_fields
    - All fields are instance of Field
    - Fields size is as same as meta.get_size()

    3. get_colnames
    - column names are matched with Field variable names
    
    4. get_index_field
    - if you set index field, model should get index field
    """
    def test_meta__size_equals_declared_field_size(self):
        class _Dummy(Model):
            col1=Field("c1")
            col2=Field("c2")
            col3=Field("c3")
        
        dummy = _Dummy()
        self.assertEqual(dummy.meta.get_size(), 3)
    
    def test_get_fields__all_fields_are_Field(self):
        dummy = DummyModel()
        
        fields = dummy.get_fields()
        is_valid = True
        for field in fields:
            if not isinstance(field, Field):
                is_valid = False
                break
        
        self.assertTrue(is_valid)
    
    def test_get_fields__fields_size_equals_meta_size(self):
        dummy = DummyModel()

        self.assertEqual(len(dummy.get_fields()), dummy.meta.get_size())


    def test_get_colnames__column_names_match(self):
        class _Dummy(Model):
            col1=Field("c1")
            col2=Field("c2")
            col3=Field("c3")
        
        dummy = _Dummy()
        is_valid = True
        for name in dummy.get_colnames():
            if not name in ["col1", "col2", "col3"]:
                is_valid = False
                break

        self.assertTrue(is_valid)
    
    def test_index_should_not_include_at_colnames(self):
        """
        Index has no target name. So index should not include at column names.
        """
        class _Dummy(Model):
            col1=Field(index=True)
            col2=Field("c1")
            col3=Field("c2")
            col4=Field("c3")
        
        dummy = _Dummy()
        columns = ["col2", "col3", "col4"]
        is_valid = True
        for name in dummy.get_colnames():
            if not name in columns:
                is_valid = False
                break
        
        self.assertTrue(is_valid)
    
    def test_index_field(self):
        class _Dummy(Model):
            col1=Field(index=True)
            col2=Field("c1")
            col3=Field("c2")
            col4=Field("c3")
        
        dummy = _Dummy()
        field = dummy.get_index_field()
        self.assertTrue(field is not None)


class FieldTests(unittest.TestCase):
    """
    Field is constructed in Model static variables.
    So you have to check Field constructor arguments.

    - target: The target of the column name from the origin file. Default value is None
    - change: It is the function that has the target parameter that returns converted value. Default value is None
    ```python
    def change_value(target):
        write some codes
        ...
    change=change_value
    ```
    - index: If index = True, auto_increment, generator is referenced. Default value is False.
    - auto_increment: If True, it ignores target column name and replace the auto_increment integer.
    - generator: If you have random generated function, you can set this argument to create random ID.
    ```python
    def random_generator():
        write some codes
        ...
    generator=random_generator
    ```
    """

    def test_init_arguments(self):
        argspec = inspect.getfullargspec(Field.__init__)
        is_value = True
        args = [
            "target",
            "change",
            "index",
            "auto_increment",
            "generator"
        ]
        for arg in args:
            if arg not in argspec.args:
                is_value = False
                break
        self.assertTrue(is_value)


class ManagerTests(unittest.TestCase):
    """
    There is a bunch of steps to pre-processing DataFrame data structure

    1. Remove columns that is not matched
    2. Replace column name
    3. Replace value
    4. Add index if model has index_field
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

    def test_replace_value(self):
        model = DummyModel()
        df = pd.read_csv(test_file)

        manager = Manager(model, df)
        manager.steps[0]()
        manager.steps[1]()
        manager.steps[2]()

        is_valid = True
        for i in manager.get()["name"]:
            if not i.startswith("_"):
                is_valid = False
                break
        self.assertTrue(is_valid)
    
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
        manager.steps[3]()

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
        manager.steps[3]()

        for i in range(len(df)):
            self.assertTrue(isinstance(df.index.to_list()[i], uuid.UUID))


if __name__ == "__main__":
    unittest.main()
