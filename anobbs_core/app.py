import json
import logging
import time

import click

from anobbs_core import AppConstant
from anobbs_core.lib import BbsManager

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

    token = bm.login(bm.get_admin_account().id)
    # admin = bm.get_account_by_token(token.id)
    # ic = bm.create_invitation_code_by_token(token.id)
    # if not admin.ac_id_list:
    #     ac_id = bm.create_ano_code_by_token(token.id).id
    # else:
    #     ac_id = admin.ac_id_list[0]
    # page = bm.post_page(token.id, ac_id, f"Good day! Now time: {time.time()}")
    # for i in range(32):
    #     page = bm.append_page(page.id, token.id, ac_id, f"Yes, {i} times")

    # print(json.dumps(bm.get_page_with_floors(page.id, 10, 1), indent=2))
    # print(json.dumps(bm.get_page_with_floors(page.id, 10, 2), indent=2))
    print(json.dumps(bm.get_group_with_pages("all", 1000, 1), indent=2))
    # print(json.dumps(bm.get_display_account_by_token(token.id), indent=2))
    # bm.show()

    exit(0)


if __name__ == '__main__':
    cli()
