from tests.test_migrations import util


def test_files():
    assert len(util.get_migrations()) == 4
