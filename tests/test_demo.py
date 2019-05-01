from importlib import import_module

import pytest

from demo import get_product_from_openfoodfacts

class MyMonkeyPatch:
    """Monkey patches a callable."""

    def __init__(self):
        """Initializes the instance."""
        self._callable = None
        self._module = None
        self._original_callable = None

    def setattr(self, import_string, mock):
        """Monkey patches a given callable by a mock."""
        mod, self._callable = import_string.rsplit(".", maxsplit=1)
        self._module = import_module(mod)
        self._original = getattr(self._module, self._callable)
        setattr(self._module, self._callable, mock) 

    def reset(self):
        """Reverses the monkey patching, reassigning back the original callable to its identifier."""
        setattr(self._module, self._callable, self._original)


@pytest.fixture
def mymonkeypatch():
    """Reproduces naively the behaviour of the monkypatch fixture from pytest."""
    mk =  MyMonkeyPatch()

    yield mk

    mk.reset()


def test_get_product_from_openfoodfacts_returns_list_with_produit1(mymonkeypatch):
    class MockGet:

        def __init__(self, url, params):
            self.status_code = 200

        def json(self):
            return {
                "products": [
                    {"product_name": "Produit 1"},
                    {"product_name": "Produit 2"},
                    {"product_name": "Produit 3"},
                ]
            }

    mymonkeypatch.setattr('requests.get', MockGet)
    result = get_product_from_openfoodfacts("pizza")
    assert len(result) == 3
    assert result[0]["product_name"] == "Produit 1"