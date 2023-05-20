import typing
from rand.providers.base import RandProxyBaseProvider, BaseRandAdapter

if typing.TYPE_CHECKING:  # pragma: no cover
    from rand import Rand


class ENTarget(BaseRandAdapter):
    def __init__(self, rand: 'Rand' = None):
        super().__init__(rand=rand)

    def vocal(self):
        vocals = 'aiueo'
        return self._rand.random.choice(list(vocals) + list(vocals.upper()))

    def consonant(self):
        consonants = 'bcdfghjklmnpqrstvwxyz'
        return self._rand.random.choice(list(consonants) + list(consonants.upper()))


class ENProvider(RandProxyBaseProvider):
    def __init__(self, prefix: str = 'en', target=None):
        target = target if target else ENTarget()
        super(ENProvider, self).__init__(prefix=prefix, target=target)
