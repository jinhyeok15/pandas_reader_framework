from io import StringIO
from model import Model, Field

in_mem_csv = StringIO("""\
col1,col2,col3
1,3,foo
2,5,bar
-1,7,baz""")


class DummyModel(Model):
    id = Field(index=True, auto_increment=True)
    name = Field("학부_과(전공)명", change=lambda x: "_" + x)
    univ = Field("학교명")
    college = Field("단과대학명")
    investigation_year = Field("조사년도")


table = [
    ["학부_과(전공)명", "학교명", "단과대학명", "조사년도"],
    ["a1", "b1", "c1", "d1"],
    ["a2", "b2", "c2", "d2"],
    ["a3", "b3", "c3", "d3"],
    ["a4", "b4", "c4", "d4"],
    ["a5", "b5", "c5", "d5"]
]
