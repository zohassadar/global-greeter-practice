"""
What what
"""
from __future__ import annotations

import dataclasses

import jinja2


@dataclasses.dataclass
class Recipient:
    """Used to simplify storing a recipient string"""

    recipient: str
    """The string containing the recipient information"""
    recipients: int = 0
    """Unused: future optional number of recipients"""
    recipient_list: list[str] = dataclasses.field(default_factory=list)
    """Unused: list of recpients, default is an empty list"""


def main():
    "This is the main function that does things"
    env = jinja2.Environment(
        loader=jinja2.PackageLoader("greeter"),
    )
    template = env.get_template("greet.j2")
    recipient = Recipient("Planet")
    print(template.render(recipient=recipient.recipient))
