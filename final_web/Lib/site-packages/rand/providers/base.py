import re
import typing

if typing.TYPE_CHECKING:  # pragma: no cover
    from rand import Rand, ParseFnType


class BaseRandAdapter:
    _rand: typing.Optional['Rand']

    def __init__(self, rand: 'Rand' = None):
        self._rand = rand

    @property
    def rand(self):
        return self._rand

    @rand.setter
    def rand(self, rand):
        self._rand = rand


class RandBaseProvider(BaseRandAdapter):
    _prefix: str

    def __init__(self, prefix: str = ''):
        super(RandBaseProvider, self).__init__()
        self.prefix = prefix

    @property
    def prefix(self) -> str:
        return self._prefix

    @prefix.setter
    def prefix(self, prefix: str):
        self._prefix = prefix

    def get_parse_name(self, name: str) -> typing.Optional[str]:
        # name always start with _parse_[PREFIX], normalise first
        name = re.sub('^_parse_', '', name)
        if name.startswith(self.prefix):
            name = re.sub('^%s_' % self.prefix, '', name)
            return name
        return None

    def parse(self, name: str, pattern: any, opts: dict):  # pragma: no cover
        return None

    def register(self):  # pragma: no cover
        pass


class RandProxyBaseProvider(RandBaseProvider):
    def __init__(self, prefix: str = '', target=None):
        super(RandProxyBaseProvider, self).__init__(prefix=prefix)
        self.target = target

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    def proxy_parse(self, name: str):
        def parse(pattern, opts):
            token, args = opts['token'], opts['args']
            # name can be acquired from the pattern token, commented out for clarity
            # name = token.replace('%s_' % self._prefix, '')
            fn = getattr(self._target, name.replace('%s_' % self._prefix, ''))
            if fn:
                if isinstance(args, list):
                    return fn(*args)
                elif isinstance(args, dict):
                    return fn(**args)
                else:
                    return fn()
        return parse

    def parse(self, name: str, pattern: any, opts: dict):
        # name always start with _parse_[PREFIX], normalise first
        parsed_name = self.get_parse_name(name)
        if parsed_name and callable(getattr(self._target, parsed_name, None)) and not parsed_name.startswith('_'):
            return self.proxy_parse(parsed_name)(pattern, opts)
        return None

    def register(self):
        # registering parse can be explicit like this or by dynamic with get_parse (this is newer and flexible way)
        # this code commented out for clarity
        # names = [
        #     name for name in dir(self._target)
        #     if callable(getattr(self._target, name))
        #     if not name.startswith('_')
        # ]
        # for name in names:
        #     self.rand.register_parse('%s_%s' % (self._prefix, name), self.proxy_parse(name=name))
        pass
