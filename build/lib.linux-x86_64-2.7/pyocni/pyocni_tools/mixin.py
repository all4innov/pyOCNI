def mixIn(base, addition):
    """Mixes in place, i.e. the base class is modified.
    Tags the class with a list of names of mixed members.
    """
    assert not hasattr(base, '_mixed_')
    mixed = []
    for item, val in addition.__dict__.items():
        if not hasattr(base, item):
            setattr(base, item, val)
            mixed.append(item)
    base._mixed_ = mixed


def unMix(cla):
    """

    Undoes the effect of a mixin on a class. Removes all attributes that
    were mixed in -- so even if they have been redefined, they will be
    removed.

    """
    #_mixed_ must exist, or there was no mixin
    for m in cla._mixed_:
        delattr(cla, m)
    del cla._mixed_


def mixedIn(base, addition):
    """

    Same as mixIn, but returns a new class instead of modifying
    the base.

    """

    class newClass:
        pass

    newClass.__dict__ = base.__dict__.copy()
    mixIn(newClass, addition)
    return newClass
