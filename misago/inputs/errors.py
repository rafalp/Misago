from typing import Dict, List, Optional, Union


class InputError(Exception):
    code: str

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)

    def __bool__(self) -> bool:
        return True

    def unwrap(self) -> str:
        return self.code


class Errors:
    def __bool__(self):
        raise NotImplementedError("Errors container has to override '__bool__' method.")

    def unwrap(self):
        raise NotImplementedError("Errors container has to override 'unwrap' method.")


Error = Union[InputError, List["Error"], Dict[str, "Error"]]
UnwrappedError = Union[str, List["UnwrappedError"], Dict[str, "UnwrappedError"]]


class ErrorsList(Errors):
    _errors: List[Error]

    def __init__(self, errors: Optional[List[Error]] = None):
        self._errors = errors or []

    def __bool__(self) -> bool:
        return bool(self._errors)

    def add_error(self, error: InputError):
        self._errors.append(error)

    def unwrap(self) -> List[UnwrappedError]:
        return [e.unwrap() for e in self._errors]


class ErrorsMap(Errors):
    _errors: Dict[str, Error]

    def __init__(self):
        self._errors = {}

    def __bool__(self) -> bool:
        for value in self._errors.values():
            if bool(value):
                return True

        return False

    def add_error(self, field_name: str, error: InputError):
        self._errors.setdefault(field_name, ErrorsList()).append(error)

    def unwrap(self) -> Dict[str, UnwrappedError]:
        return {field: errors.unwrap() for field, errors in self._errors.items()}
