from crate import store
from crate.models import Track


def test_add_and_load_preserves_order(tmp_path):
    conn = store.connect(tmp_path / "test.db")
    store.add_track(conn, "warmup", Track("A", "X", 120))
    store.add_track(conn, "warmup", Track("B", "Y", 124))
    assert [t.title for t in store.load_crate(conn, "warmup").tracks] == ["A", "B"]
