from rand.providers.base import RandProxyBaseProvider


class RandFakerProvider(RandProxyBaseProvider):
    def __init__(self, prefix: str = 'faker', target=None):
        from faker import Faker
        target = target if target else Faker()
        super(RandFakerProvider, self).__init__(prefix=prefix, target=target)
