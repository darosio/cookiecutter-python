"""Command-line entries for the module."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import click


@click.group()
@click.pass_context
@click.version_option(message="%(version)s")
@click.option("--verbose", "-v", count=True, help="Verbosity of messages.")
@click.option("--out", "-o", type=cPath(), help="Output folder.")
def ppr(ctx: Context, verbose: int, out: str) -> None:  # pragma: no cover
    """Parse Plate Reader `ppr` group command."""
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    if out:
        ctx.obj["OUT"] = out

@ppr.command()
@click.pass_context
@click.argument("list_file", type=cPath(exists=True))
