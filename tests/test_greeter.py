import global_greeter.greet


def test_greet_main_output(capsys):
    global_greeter.greet.main()
    captured = capsys.readouterr()
    assert captured.out == "Hi Planet\n"
