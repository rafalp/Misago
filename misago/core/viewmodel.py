class ViewModel:
    def __getattr__(self, name):
        return getattr(self._model, name)

    def unwrap(self):
        return self._model
