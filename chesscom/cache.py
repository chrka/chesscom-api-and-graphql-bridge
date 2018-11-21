from typing import TypeVar, Generic, Callable, Optional
from datetime import datetime, timedelta


def cached(decorated_cls):
    """Turn a class into its cached counterpart.

    A decorated class keeps a unique instance per key. This is a bit overly
    complicated, but is convenient while developing the API since we don't need
    to add separate `lookup_*` functions until we are sure which ones we want.
    """

    def __cached_new(cls, key):
        # Consistent use of lower case for string keys
        lookup_key = key.lower() if isinstance(key, str) else key

        if lookup_key in cls._instance_cache:
            return cls._instance_cache[lookup_key]

        instance = super(decorated_cls, cls).__new__(cls)
        # Use original key when creating instance. Mainly for debugging,
        # need to make an API call to get proper capitalization, or to even
        # check if the entity exists — and we want to postpone calling the API
        # for as long as possible!
        cls._initializer(instance, key)

        cls._instance_cache[lookup_key] = instance

        return instance

    def __cached_init(cls, key):
        pass

    decorated_cls._instance_cache = {}
    decorated_cls._initializer = decorated_cls.__init__
    decorated_cls.__new__ = __cached_new
    decorated_cls.__init__ = __cached_init
    return decorated_cls


T = TypeVar('T')


class Requested(Generic[T]):
    """Keeps cached values. Does not flush expired values."""
    requester: Callable[[], None]
    received: Optional[datetime]
    data: Optional[T]

    def __init__(self, requester: Callable[[], None], ttl=7200) -> None:
        """Initialize an expiring value with a requester function."""
        self.requester = requester
        self.received = None
        self.data = None
        self.ttl = timedelta(seconds=ttl)

    def has_data(self):
        """Chech if there is a non-expired value available."""
        return self.received and self.age() < self.ttl

    def __call__(self) -> T:
        """Return the value, fetching it first if needed."""
        if self.has_data():
            return self.data
        else:
            self.requester()
            if not self.has_data():
                raise Exception()
            else:
                return self.data

    def receive(self, data: T) -> None:
        """Store a value."""
        self.received = datetime.now()
        self.data = data

    def age(self, until=None) -> Optional[timedelta]:
        """The age of the value, if any."""
        if not self.received:
            return None

        if not until:
            until = datetime.now()

        return until - self.received
