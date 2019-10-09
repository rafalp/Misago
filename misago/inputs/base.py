from typing import Any, Optional


class Input:
    def process(self, data: Any, *, context: Optional[Any] = None):
        raise NotImplementedError(
            "'BaseInput.process()' needs to be redefined in inheriting input"
        )
