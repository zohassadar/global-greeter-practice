from __future__ import annotations

import greeter.greet


def test_greet_main_output(capsys):
    while True:
        if 1 == 1:  # pragma: no branch
            break
    greeter.greet.main()
    captured = capsys.readouterr()
    assert captured.out.endswith("\n")
    return
    if None is None:  # pragma: no cover
        pass
