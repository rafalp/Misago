class FormIterator(object):
    def __init__(self, form, fieldsets=None):
        self._index = -1
        self.form = form
        try:
            self.fieldsets = fieldsets or form.fieldsets
        except AttributeError:
            raise AttributeError('Form fieldset could not be found. Either pass explicit "fieldsets" argument to FormIterator or define "fieldsets" attribute on form.')

    def __iter__(self):
        return self

    def next(self):
        self._index += 1
        try:
            return FieldsetIterator(self.form,
                                    self.fieldsets[self._index][0],
                                    self.fieldsets[self._index][1])
        except IndexError:
            self._index = -1
            raise StopIteration()


class FieldsetIterator(object):
    def __init__(self, form, name, fields):
        self._index = -1
        self.form = form
        self.name = name
        self.fields = fields

    def __iter__(self):
        return self

    def next(self):
        self._index += 1
        try:
            row =  self.fields[self._index]
            if isinstance(row, basestring):
                field_name = row
                return self.form[field_name]
            field_name = row[0]
            field = self.form[field_name]
            field.extra =  row[1]
            return field
        except IndexError:
            raise StopIteration()
        except KeyError:
            raise KeyError('Field "%s" could not be found in iterated form.' % field_name)