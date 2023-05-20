import re
import typing
from peewee import Proxy, fn, IntegerField, CharField, Model

from rand.providers.base import RandProxyBaseProvider, BaseRandAdapter

if typing.TYPE_CHECKING:  # pragma: no cover
    from rand import Rand, ParseFnType


class DatasetTarget(BaseRandAdapter):
    def get(self, name: str):  # pragma: no cover
        pass


class ListDatasetTarget(DatasetTarget):
    db: dict

    def __init__(self, db: dict = None, rand: 'Rand' = None):
        super().__init__(rand=rand)
        self.db = db if db else {}

    def get(self, name: str):
        table = self.db.get(name, [])
        row = self.rand.random.choice(table)
        return row.get('name') if row else None


class DBDatasetTarget(DatasetTarget):
    db: Proxy

    def __init__(self, db: Proxy = None, rand: 'Rand' = None):
        super().__init__(rand=rand)
        self.db = db if db else Proxy()

    def _create_table(self, name: str):
        NameModel = type(name, (Model,), {
            'id_': IntegerField(primary_key=True, column_name='id'),
            'name': CharField(column_name='name')
        })
        table: Model = NameModel()
        table.bind(self.db)
        return table

    def get(self, name: str):
        table = self._create_table(name=name)
        row = table.select().order_by(fn.Random()).get()
        return row.name


class RandDatasetBaseProvider(RandProxyBaseProvider):
    def __init__(self, prefix: str = 'ds', target=None):
        target = target if target else DatasetTarget()
        super(RandDatasetBaseProvider, self).__init__(prefix=prefix, target=target)

    def parse(self, name: str, pattern: any, opts: dict):
        parsed_name = self.get_parse_name(name)
        if parsed_name and parsed_name.startswith('get_'):
            # if name in format of get_[NAME]
            parsed_name = re.sub('^get_', '', parsed_name)
            target: DatasetTarget = self.target
            return target.get(parsed_name)
        return super().parse(name=name, pattern=pattern, opts=opts)
