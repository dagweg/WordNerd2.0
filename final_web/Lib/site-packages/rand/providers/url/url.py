import re
import typing
import requests

from rand.providers.base import RandProxyBaseProvider, BaseRandAdapter

if typing.TYPE_CHECKING:  # pragma: no cover
    from rand import Rand, ParseFnType


class UrlTarget(BaseRandAdapter):
    urls: dict

    def __init__(self, urls: dict = None, rand: 'Rand' = None):
        super().__init__(rand=rand)
        self.urls = urls if urls else {}

    def get(self, name: str):
        url = self.urls.get(name)
        print(self.urls, name)
        if url:
            data = []
            try:
                # expecting JSON data with format of
                # {
                #   "data": [
                #     "test",
                #     "test"
                #   ]
                # }
                data = requests.get(url).json().get('data')
            except ValueError:
                pass
            if not data:
                try:
                    # expecting JSON data with format of
                    # test
                    # test
                    # test
                    data = requests.get(url).text
                    if isinstance(data, str):
                        data = data.splitlines()
                except ValueError:
                    pass
            if data and len(data) > 0:
                return self.rand.random.choice(data)
        return None


class RandUrlBaseProvider(RandProxyBaseProvider):
    def __init__(self, prefix: str = 'url', target=None):
        target = target if target else UrlTarget()
        super(RandUrlBaseProvider, self).__init__(prefix=prefix, target=target)

    def parse(self, name: str, pattern: any, opts: dict):
        parsed_name = self.get_parse_name(name)
        if parsed_name and parsed_name.startswith('get_'):
            # if name in format of get_[NAME]
            parsed_name = re.sub('^get_', '', parsed_name)
            target: UrlTarget = self.target
            return target.get(parsed_name)
        return super().parse(name=name, pattern=pattern, opts=opts)
