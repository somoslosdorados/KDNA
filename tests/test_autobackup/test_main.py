import click
from click.testing import CliRunner


def test_greet():
    @click.command()
    @click.argument('name')
    def greet(name):
        click.echo('Hello %s' % name)

    runner = CliRunner()
    result = runner.invoke(greet, ['Sam'])
    assert result.output == 'Hello Sam\n'


if __name__ == '__main__':
    test_greet()
