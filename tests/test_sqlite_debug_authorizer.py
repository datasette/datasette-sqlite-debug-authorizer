from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_plugin_is_installed(capsys):
    datasette = Datasette(memory=True)
    response = await datasette.client.get("/_memory.json?sql=select+1")
    assert response.status_code == 200
    captured = capsys.readouterr().err
    # There should be all sorts of stuff in there
    for expected in (
        "SQLITE_SELECT:",
        'SQLITE_READ:  table="sqlite_master"',
        "SQLITE_PRAGMA:",
    ):
        assert expected in captured
