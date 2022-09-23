from __future__ import annotations

import jinja2


def main():
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("greeter"),
    )
    template = env.get_template("greet.j2")
    print(template.render(recipient="Planet"))
