from types import SimpleNamespace
from typing import List, Optional

from fixtup.prompt.base import Prompt


p_store = SimpleNamespace()
p_store.input = []


def reset_input() -> None:
    """
    reset inputs given by the user in the automated test
    """
    p_store.input = []


def send_text(input: str):
    p_store.input.append(input)


class Mock(Prompt):
    """
    Fake implementation of a prompt to perform unit test that
    requires user input
    """

    def choice(self, question: str, choices: List[str], default: Optional[str] = None) -> str:
        mocked_input: List[str] = p_store.input
        _input = mocked_input.pop(0)
        assert _input in choices, f"{_input} does not match the available choices {choices}"

        return _input

    def fixture_repository(self) -> str:
        mocked_input: List[str] = p_store.input
        return mocked_input.pop(0)

    def new_fixture(self, fixture_repository: str) -> str:
        mocked_input: List[str] = p_store.input
        return mocked_input.pop(0)

    def confirm(self, question: str, default: bool = False) -> bool:
        mocked_input: List[str] = p_store.input
        _input = mocked_input.pop(0)
        if _input == "":
            return default
        else:
            return _input == "y"

    def input(self, question: str, default: Optional[str] = None) -> Optional[str]:
        mocked_input: List[str] = p_store.input
        _input = mocked_input.pop(0)
        if _input == "":
            return default
        else:
            return _input
