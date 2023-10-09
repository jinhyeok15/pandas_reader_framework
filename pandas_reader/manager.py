import os
from typing import Optional
import pandas as pd
from pandas import RangeIndex

from pandas_reader.model import Model
from pandas_reader.setup import config


def _get_dataframe(filename: str) -> Optional[pd.DataFrame]:
    """
    Pre-precessing from the ./sources.

    If you want to change default case of type, you can try it as you can.

    This framework provides you to choice below
    - csv
    - excel
    - json
    """
    file_type = config.FILETYPE
    source_path = config.SOURCE_PATH

    path = os.path.join(config.BASE_DIR, source_path, filename)

    if file_type == "csv":
        df = pd.read_csv(path, **config.PANDAS_READ_OPTIONS)
        return df
    if file_type == "excel":
        df = pd.read_excel(path, engine='openpyxl', **config.PANDAS_READ_OPTIONS)
        return df
    if file_type == "json":
        df = pd.read_json(path, **config.PANDAS_READ_OPTIONS)
        return df


class Manager:
    def __init__(self, model: Model, df: pd.DataFrame):
        self._model = model
        self._df = df
        self._target_colnames = []
        self._colnames = model.get_colnames()
        self._mapper = {}

        self._fields = model.get_fields()

        for i, field in enumerate(self._fields):
            self._target_colnames.append(field.target)
            self._mapper[field.target] = self._colnames[i]

    def _remove_unmatched_column(self) -> None:
        self._df = self._df.loc[:, self._target_colnames]


    def _replace_column_name(self) -> None:
        self._df.rename(columns=self._mapper, inplace=True)


    def _replace_value(self) -> None:
        columns = self._colnames
        for i, field in enumerate(self._fields):
            if field.change:
                pool = self._df[columns[i]].unique().tolist()
                for v in pool:
                    self._df[columns[i]] = self._df[columns[i]].replace(v, field.change(v))

    def _set_index(self) -> None:
        field = self._model.get_index_field()
        if not field:
            return

        if field.auto_increment:
            self._df.index = RangeIndex(1, len(self._df)+1, 1)

        if field.generator:
            self._df.index = [field.generator() for _ in range(len(self._df))]
    
    def _filter_rows(self) -> None:
        dropped_index = []
        filter_confs = []
        for i, field in enumerate(self._fields):
            if field.filter:
                filter_confs.append((field.filter, self._colnames[i]))

        for idx in self._df.index:
            for filter, c in filter_confs:
                if not filter(self._df[c][idx]):
                    dropped_index.append(idx)
                    break
        self._df = self._df.drop(dropped_index)

    def get(self):
        return self._df
    
    @property
    def steps(self):
        return [
            self._remove_unmatched_column,
            self._replace_column_name,
            self._set_index,
            self._replace_value,
            self._filter_rows
        ]


def fetch(model: Model, filename=None):
    df = _get_dataframe(filename)
    manager = Manager(model, df)
    for step in manager.steps:
        step()
    return manager.get()
