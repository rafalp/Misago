class MutableFields(object):
    @classmethod
    def subset_fields(cls, *fields):
        fields_in_name = [f.title().replace('_', '') for f in fields]
        name = '{}{}Subset'.format(cls.__name__, ''.join(fields_in_name)[:100])

        class Meta(cls.Meta):
            pass

        Meta.fields = list(fields)

        return type(name, (cls, ), {'Meta': Meta})

    @classmethod
    def exclude_fields(cls, *fields):
        final_fields = []
        for field in cls.Meta.fields:
            if field not in fields:
                final_fields.append(field)

        fields_in_name = [f.title().replace('_', '') for f in final_fields]
        name = '{}{}Subset'.format(cls.__name__, ''.join(fields_in_name)[:100])

        class Meta(cls.Meta):
            pass

        Meta.fields = list(final_fields)

        return type(name, (cls, ), {'Meta': Meta})

    @classmethod
    def extend_fields(cls, *fields):
        final_fields = list(cls.Meta.fields)
        for field in fields:
            if field not in final_fields:
                final_fields.append(field)

        fields_in_name = [f.title().replace('_', '') for f in final_fields]
        name = '{}{}Subset'.format(cls.__name__, ''.join(fields_in_name)[:100])

        class Meta(cls.Meta):
            pass

        Meta.fields = list(final_fields)

        return type(name, (cls, ), {'Meta': Meta})
