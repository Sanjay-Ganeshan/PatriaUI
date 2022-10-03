def use_passed_or_default(passed, **defaults):
    new_kwargs = {}
    new_kwargs.update(defaults)
    new_kwargs.update(passed)
    return new_kwargs
