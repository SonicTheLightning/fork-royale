from fork_royale.cli.main import main


def test_cli_runs_headless(capsys):
    result = main(["--ticks", "2", "--no-render"])
    output = capsys.readouterr().out
    assert result == 0
    assert "Result:" in output or "Stopped after" in output
