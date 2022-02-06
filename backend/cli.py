from os import path

import typer
import uvicorn
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from alembic import command
from alembic.config import Config
from fief import __version__
from fief.app import app as fief_app
from fief.models import Account
from fief.services.account_db import AccountDatabase
from fief.settings import settings

alembic_config_file = path.join(path.dirname(__file__), "alembic.ini")

app = typer.Typer()


@app.command()
def info():
    """Show current Fief version and settings."""
    typer.secho(f"Fief version: {__version__}", bold=True)
    typer.secho(f"Settings", bold=True)
    for key, value in settings.dict().items():
        typer.echo(f"{key}: {value}")


@app.command("migrate-global")
def migrate_global():
    """Apply database migrations to the global database."""
    engine = create_engine(settings.get_database_url(False))
    with engine.begin() as connection:
        alembic_config = Config(alembic_config_file, ini_section="global")
        alembic_config.attributes["connection"] = connection
        command.upgrade(alembic_config, "head")


@app.command("migrate-accounts")
def migrate_accounts():
    """Apply database migrations to each account database."""
    engine = create_engine(settings.get_database_url(False))
    Session = sessionmaker(engine)
    with Session() as session:
        account_db = AccountDatabase()
        accounts = select(Account)
        for [account] in session.execute(accounts):
            assert isinstance(account, Account)
            typer.secho(f"Migrating {account.name}", bold=True)
            account_db.migrate(
                account.get_database_url(False), account.get_schema_name()
            )


@app.command("run-server")
def run_server(host: str = "0.0.0.0", port: int = 8000):
    """Run the Fief backend server."""
    uvicorn.run(fief_app, host=host, port=port)


if __name__ == "__main__":
    app()