import logging
import random

import click

from anonymous_bbs import AppConstant
from anonymous_bbs.lib import BbsManager

logger = logging.getLogger(__name__)


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(AppConstant.NAME)
    click.echo(AppConstant.VERSION)
    click.echo()
    ctx.exit(0)


def set_debug_level(debug: str) -> None:
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s: %(message)s')


@click.command()
@click.option("--version",
              is_flag=True,
              callback=print_version,
              expose_value=False,
              is_eager=True)
@click.option("-d",
              "--debug",
              is_flag=True,
              help="Start debug mode")
@click.pass_context
def cli(
        ctx,
        debug,
):
    ctx.ensure_object(dict)
    set_debug_level(debug)

    bm = BbsManager()
    last_ac = None
    ra = bm.create_root_account()
    for _ in range(random.randint(5, 10)):
        ic = bm.create_ic(ra.id)
        if random.randint(0, 1) == 0:
            na = bm.create_account_by_ic(ic.id)
            for _ in range(random.randint(1, 2)):
                last_ac = bm.create_ac(na.id)

    if last_ac:
        page = bm.post_page(last_ac.id, "HHHHHHHH", "new_group")
        for i in range(20):
            bm.append_page(page.id, last_ac.id, f"Floor: {i}")

    old_token = bm.login(ra.id)
    print(old_token.to_dict())
    ra_id = bm.get_owner_id_by_token_id(old_token.id)
    new_token = bm.login(ra_id)

    print(new_token.id)
    print(bm.get_owner_id_by_token_id(old_token.id))

    bm.show()

    exit(0)


if __name__ == '__main__':
    cli()
