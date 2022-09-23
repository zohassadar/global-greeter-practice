from __future__ import annotations

import greeter.greet


def test_greet_main_output(capsys):
    greeter.greet.main()
    captured = capsys.readouterr()
    assert captured.out.endswith("\n")
