from typing import List


class Field:
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
    def __init__(self,
                 target=None,
                 change=None,
                 index=False,
                 auto_increment=True,
                 generator=None):
        self.target = target
        self.change = change
        self.index = index
        self.auto_increment = auto_increment
        self.generator = generator


class ModelMeta:
    def __init__(self, __model_class__):
        self._columns = []
        self._fields = []
        self._index_field = None
        model_vars = vars(__model_class__)
        for k, v in model_vars.items():
            if isinstance(v, Field):
                if v.index:
                    self._index_field = v
                    continue
                self._columns.append(k)
                self._fields.append(v)
        self._size = len(self._columns)

    def get_size(self):
        return self._size


class Model:
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
    """
    def __init__(self):
        self.meta = ModelMeta(self.__class__)
    
    def get_fields(self) -> List[Field]:
        return self.meta._fields
    
    def get_colnames(self):
        return self.meta._columns
    
    def get_index_field(self):
        return self.meta._index_field
