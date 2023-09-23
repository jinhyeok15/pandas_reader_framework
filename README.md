# Pandas reader framework

> Framework for converting file to dataframe

## Scenario

The purpose of this script program is to extract the dataframe that is pre-processed.
What I want to expect from this program is complying with scenario like below.

1. Read file and convert to pandas.DataFrame.
2. Changing column name that is used by domain or database.
3. Changing value from the column.
4. Filtering rows

To approach this purpose, you don't need to know about the pandas api.
You just need to declare Field in the Model class, and get the result by executing main.py.

## Guide

### Setup data file

Setup data file which is located at './sources/'

Then, write the code on **snapshot.py**

### Import module

``` python
from pandas_reader.model import Model
```

### Use case

Inherit Model class, and define static variables(instance of Field) in Model.

```python
class Major(Model):
    id = Field(index=True, auto_increment=True)
    name = Field("학부_과(전공)명")
    univ = Field("학교명")
    department = Field("단과대학명")
    investigation_year = Field("조사년도")
    sido_code = Field("지역", change=change_location_to_sido_code)
    status = Field("학과상태", change=change_status)
    std_clsf_name = Field("표준분류대계열")
```

Register Model instance and filename in configs.py

``` python
from implement import Student

MODEL_INSTANCE = Student()
FILNAME = "students.csv"
```

### Run script

```console
python main.py
```

You can get the dataframe result.

```console
        name            univ  college  investigation_year sido_code  status std_clsf_name
1      멀티미디어통신학과        ICT폴리텍대학  단과대구분없음                2022        31  ACTIVE          공학계열
2        모바일통신학과        ICT폴리텍대학  단과대구분없음                2022        31  DELETE          공학계열
3        스마트통신학과        ICT폴리텍대학  단과대구분없음                2022        31  ACTIVE          공학계열
4         이동통신학과        ICT폴리텍대학  단과대구분없음                2022        31  ACTIVE          공학계열
5         정보보안학과        ICT폴리텍대학  단과대구분없음                2022        31  ACTIVE          공학계열
...          ...             ...      ...                 ...       ...     ...           ...
49625      기독교학과  횃불트리니티신학대학원대학교  단과대구분없음                2022        11  ACTIVE        인문사회계열
49626       목회학과  횃불트리니티신학대학원대학교  단과대구분없음                2022        11  ACTIVE        인문사회계열
49627        신학과  횃불트리니티신학대학원대학교  단과대구분없음                2022        11  ACTIVE        인문사회계열
49628     예배음악학과  횃불트리니티신학대학원대학교  단과대구분없음                2022        11  ACTIVE        인문사회계열
49629      일반신학과  횃불트리니티신학대학원대학교  단과대구분없음                2022        11  ACTIVE        인문사회계열

[49629 rows x 7 columns]
```

## Document

### Model

Manager uses Model to change columns and values by checking the Field element.
So you need to check model instance properties.

1. meta

- Model information should follow the declaration

2. get_fields

- All fields are instance of Field
- Fields size is as same as meta.get_size()

3. get_colnames

- column names are matched with Field variable names

### Field

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
Filter is applied after the change function executed.

### Manager

1. Get dataframe from file

If you want to change the default setting, just do it.
the keyword argument of _get_dataframe function is allied to pandas.

2. Manager

There is a bunch of steps to pre-processing DataFrame data structure

- 1. Setup

  - Remove columns that is not matched
  - Replace column name
  - Add index if model has index_field

- 2. Iteration
  - Replace value
  - Filter rows

3. fetch

fetch function is used for main.py. It can access Manager instance, and get pre-processed dataframe data structure
