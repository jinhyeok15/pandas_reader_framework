import unittest, inspect

from pandas_reader.model import Model, Field
from pandas_reader.fixtures.fakes import DummyModel


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

    Field("Column1", change=change_value)
    ```

    - index: If index = True, auto_increment, generator is referenced. Default value is False.
    - auto_increment: If True, it ignores target column name and replace the auto_increment integer.
    - generator: If you have random generated function, you can set this argument to create random ID.

    ```python
    def random_generator():
        write some codes
        ...

    Field("Column1", generator=random_generator)
    ```

    - filter: Use this argument if you want to get values only follow some condition.
    Filter is applied after the change function executed
    Return value must be bool type

    ``` python
    def name_filter(value) -> bool:
        write some codes
        ...
    
    Field("Column1", filter=name_filter)
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
            "generator",
            "filter"
        ]
        for arg in args:
            if arg not in argspec.args:
                is_value = False
                break
        self.assertTrue(is_value)
