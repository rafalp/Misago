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

    @classmethod
    def subset_exclude(cls, *fields):
        clean_fields = []
        for field in cls.Meta.fields:
            if field not in fields:
                clean_fields.append(field)

        fields_in_name = [f.title().replace('_', '') for f in clean_fields]
        name = '{}{}Subset'.format(cls.__name__, ''.join(fields_in_name)[:100])

        class Meta(cls.Meta):
            pass

        Meta.fields = tuple(clean_fields)

        return type(name, (cls,), {
            'Meta': Meta
        })
