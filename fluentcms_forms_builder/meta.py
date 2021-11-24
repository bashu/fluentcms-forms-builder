def AbstractClassWithoutFieldsNamed(cls, *excl):
    if cls._meta.abstract:
        remove_fields = [f for f in cls._meta.local_fields if f.name in excl]
        for f in remove_fields:
            cls._meta.local_fields.remove(f)
        return cls
    else:
        raise Exception("Not an abstract model")
