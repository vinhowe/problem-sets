#  Copyright (c) 2019 Thomas Howe

import pytest

from problem_sets.serialization import serialize_recursive, _list_serializable_dict, _list_serializable_lambda, \
    Serializable


class ExampleSerializable(Serializable):

    def __init__(self, number: int, string: str):
        self.number = number
        self.string = string

    def serialize(self) -> dict:
        return self.__dict__

    @classmethod
    def deserialize(cls, serialized: dict):
        return cls(**serialized)


@pytest.fixture()
def example_serializable() -> Serializable:
    return ExampleSerializable(1, "test")


@pytest.fixture()
def example_serializable_list(example_serializable):
    return [example_serializable] * 10


@pytest.fixture()
def example_serializable_dict(example_serializable):
    return {
        "key_1": example_serializable,
        "key_2": example_serializable,
        "key_3": example_serializable,
        "key_4": example_serializable,
    }


@pytest.fixture()
def mock_data(example_serializable, example_serializable_list, example_serializable_dict):
    return {
        "unit": example_serializable,
        "list": example_serializable_list,
        "dict": example_serializable_dict,
        "test": 5
    }


@pytest.fixture()
def mock_expected_data(example_serializable, example_serializable_list, example_serializable_dict):
    return {
        "unit": example_serializable.serialize(),
        "list": _list_serializable_lambda(example_serializable_list),
        "dict": _list_serializable_dict(example_serializable_dict),
        "test": 5
    }


def test_serialize_recursive(mock_data, mock_expected_data):
    # print(self.mock_expected_data)
    serialized = serialize_recursive(mock_data)
    assert serialized == mock_expected_data
