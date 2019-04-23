import re

from data.messages import PARSE_ERROR_MSG


class CommandParser:
    def get_args(self, pattern: str, message: str) -> dict:
        result = re.match(pattern, message)
        if result is None:
            raise ValueError
        return self.transform_words(result.groupdict())

    def transform_words(self, data):
        result = {}
        for k, v in data.items():
            if '_' in v:
                result[k] = ' '.join(v.split('_'))
            else:
                result[k] = v
        return result

    def __call__(self, pattern, **kwargs):
        def outer(func):
            def inner(that, message):
                try:
                    parsed_kwargs = self.get_args(pattern, message)
                    type_mapper = func.__annotations__
                    parsed_kwargs = {
                        attr: type_mapper[attr](value)
                        if attr in type_mapper else value
                        for attr, value
                        in parsed_kwargs.items()
                    }
                except ValueError:
                    try:
                        return func(that, **kwargs)
                    except TypeError:
                        return PARSE_ERROR_MSG
                return func(that, **parsed_kwargs)

            return inner

        return outer
