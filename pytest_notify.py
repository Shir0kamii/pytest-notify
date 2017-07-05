"""Get notifications when your tests ends"""

from collections import Counter
import os
import subprocess

__version__ = "0.1.4"

counter = Counter()


def notify(title, body, icon=None):
    args = ['notify-send', title, body]
    if icon:
        if not os.path.isabs(icon):
            pwd = os.getcwd()
            os.path.join(pwd, icon)
        args += ["--icon", icon]
    subprocess.check_call(args)


def pytest_addoption(parser):
    group = parser.getgroup('notify')
    group.addoption(
        '--notify-disable',
        action='store_true',
        dest='notify_disable',
        help='Disable notifications'
    )

    parser.addini('HELLO', 'Dummy pytest.ini setting')


def pytest_runtest_logreport(report):
    if report.when == "setup" and report.outcome == "skipped":
        counter["skipped"] += 1
    if report.when != "call":
        return
    counter[report.outcome] += 1


def pytest_unconfigure(config):
    if config.option.notify_disable:
        return

    passed = counter["failed"] == 0
    title = "Tests passed" if passed else "Tests failed"

    body_parts = []
    for state in ("passed", "skipped", "failed"):
        if counter[state]:
            plural = "s" if counter[state] > 1 else ""
            msg = "{} test{} {}".format(counter[state], plural, state)
            body_parts.append(msg)

    if body_parts:
        body = "\n".join(body_parts)
        notify(title, body)
