#  Copyright (c) 2019 Thomas Howe

import pytest

from problem_sets.static.data import data_manager
from problem_sets.static.data.sqlite import sqlite_util
from problem_sets.static.data.sqlite.test.sqlite_test_util import drop_tables_list
from problem_sets.static.data.static_content_entity import StaticContentEntity, StaticContentEntityType
from problem_sets.static.data.static_problem_set_entity import StaticProblemSetEntity
from problem_sets.static.data.test import data_test_util

EXAMPLE_SET_ID = "test_id"


@pytest.fixture
def problem_set_entity():
    instruction_contents = [
        StaticContentEntity(StaticContentEntityType.text, "instruction1"),
        StaticContentEntity(StaticContentEntityType.text, "instruction2"),
        StaticContentEntity(StaticContentEntityType.text, "instruction3"),
    ]

    answer_contents = [
        StaticContentEntity(StaticContentEntityType.text, "answer1"),
        StaticContentEntity(StaticContentEntityType.text, "answer2"),
        StaticContentEntity(StaticContentEntityType.text, "answer3"),
    ]

    return StaticProblemSetEntity(EXAMPLE_SET_ID, "example source", instruction_contents, answer_contents)


def add_problem_set_to_db(problem_set_entity):
    data_manager.static_problem_set_repo.create(problem_set_entity)


def test_add_problem_set(problem_set_entity):
    data_test_util.clean_start(drop_tables_list)

    add_problem_set_to_db(problem_set_entity)

    sql_fetch = """SELECT * FROM problem_set
    """

    from problem_sets.static.data.sqlite.test.sqlite_test_util import conn

    result = sqlite_util.query_fetch(conn, sql_fetch)

    assert result is not None and len(result) == 1


def test_get_problem_set(problem_set_entity):
    data_test_util.clean_start(drop_tables_list)

    add_problem_set_to_db(problem_set_entity)

    result = data_manager.static_problem_set_repo.get(EXAMPLE_SET_ID)

    assert isinstance(result, StaticProblemSetEntity)


def test_check_problem_set_id_availability(problem_set_entity):
    data_test_util.clean_start(drop_tables_list)

    add_problem_set_to_db(problem_set_entity)

    result = data_manager.static_problem_set_repo.check_id_available(problem_set_entity.id)

    assert result is False
