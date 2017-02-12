class Subsettable(object):
    @classmethod
    def subset(cls, *fields):
        fields_in_name = [f.title().replace('_', '') for f in fields]
        name = '{}{}Subset'.format(cls.__name__, ''.join(fields_in_name)[:100])

        class Meta(cls.Meta):
            pass

        Meta.fields = fields

        return type(name, (cls,), {
            'Meta': Meta
        })
