from click.testing import CliRunner
from kdna.commands.encrypt import encrypt


def test_keygen():
    runner = CliRunner()
    result = runner.invoke(encrypt, ['key-gen'])

    assert result.exit_code == 0
    assert "Key generated" in result.output


def test_activate():
    runner = CliRunner()
    result = runner.invoke(encrypt, ['activate'])

    assert result.exit_code == 0
    assert "Encryption activated" in result.output


def test_deactivate():
    runner = CliRunner()
    result = runner.invoke(encrypt, ['deactivate'])

    assert result.exit_code == 0
    assert "Encryption deactivated" in result.output
