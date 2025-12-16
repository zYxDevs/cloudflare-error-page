import html
import secrets
from datetime import datetime, timezone
from typing import Any

from jinja2 import Environment, PackageLoader, Template, select_autoescape

env = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

default_template: Template = env.get_template("error.html")


def render(params: dict,
           allow_html: bool = True,
           template: Template | None = None,
           *args: Any,
           **kwargs: Any) -> str:
    '''Render a customized Cloudflare error page.

    :param params: Parameters passed to the template. Refer to the project homepage for more information.
    :param allow_html: Allow output raw HTML content from parameters. Set to False if you don't trust the source of the params.
    :param template: Jinja template used to render the error page. Default template will be used if ``template`` is None.
        Override this to extend or customize the base template.
    :param args: Additional positional arguments passed to ``Template.render`` function.
    :param kwargs: Additional keyword arguments passed to ``Template.render`` function.
    :return: The rendered error page as a string.
    '''
    if not template:
        template = default_template

    params = {**params}

    if not params.get('time'):
        utc_now = datetime.now(timezone.utc)
        params['time'] = utc_now.strftime("%Y-%m-%d %H:%M:%S UTC")
    if not params.get('ray_id'):
        params['ray_id'] = secrets.token_hex(8)
    if not allow_html:
        params['what_happened'] = html.escape(params.get('what_happened', ''))
        params['what_can_i_do'] = html.escape(params.get('what_can_i_do', ''))

    return template.render(params=params, *args, **kwargs)


__all__ = ['default_template', 'render']
