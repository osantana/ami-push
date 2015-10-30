# coding: utf-8


from utils import LRUCacheDict


def test_basic_lru_cache_max_size():
    pool = LRUCacheDict(max_size=3)
    pool["spam"] = 0
    assert len(pool) == 1
    assert pool["spam"] == 0

    pool["eggs"] = 1
    assert len(pool) == 2
    assert pool["eggs"] == 1

    pool["ham"] = 2
    assert len(pool) == 3
    assert pool["ham"] == 2

    pool["foo"] = 3
    assert len(pool) == 3
    assert pool["foo"] == 3
    assert "spam" not in pool


def test_basic_lru_cache_unlimited():
    pool = LRUCacheDict()
    pool["spam"] = 0
    pool["eggs"] = 1
    pool["ham"] = 2
    pool["foo"] = 3
    assert len(pool) == 4
