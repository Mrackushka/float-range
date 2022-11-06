from math import ceil


class float_range:

    def __init__ (self, *args, **kwargs):
        self.start, self.stop, self.step, self.number_type = self.__parse_args(args)
        self.__check_kwargs(kwargs)
        self.length = self.__get_length()

    def __iter__(self):
        number_amount = self.length
        i = 0
        result = self.start
        while i < number_amount:
            yield self.number_type(round(result, 10))
            result += self.step
            i += 1

    def __getitem__(self, key):
        if type(key) is slice:
            start = self[s] if (s := key.start) else self.start
            stop = self[s] if (s := key.stop) else self.stop
            step = self.step * s if (s := key.step) else self.step
            return float_range(start, stop, step)
        if key < 0:
            key = self.length + key
        if key < 0 or key >= self.length:
            raise IndexError('float_range object index out of range')
        return round(self.start + self.step * key, 10)

    def __str__(self):
        if (self.number_type is int and self.step == 1) or \
                (self.number_type is float and self.step == 0.1):
            step = ''
        else:
            step = f', {self.step}'
        return f'float_range({self.start}, {self.stop}{step})'
    
    def __repr__(self):
        return str(self)

    def __contains__(self, item):
        return item in list(self) # NotImplemented !!!

    def __len__(self):
        return self.length

    def __parse_args(self, args):
        match l := len(args):
            case 0:
                raise TypeError('float_range expected 1 argument, got 0')
            case 1 | 2 | 3:
                number_type = self.__get_number_type(args)
                step = 1 if number_type is int else 0.1
                match l:
                    case 1:
                        return 0, *args, step, number_type
                    case 2:
                        return *args, step, number_type
                    case 3:
                        return *args, number_type
            case _:
                raise TypeError(f'float_range expected at most 3 arguments, got {len(args)}')
    
    def __get_length(self):
        if (i := ceil((self.stop - self.start) / self.step)) > 0:
            return i
        return 0

    @staticmethod
    def __check_kwargs(kwargs):
        if kwargs:
            raise TypeError('float_range() takes no keyword arguments')

    @staticmethod
    def __get_number_type(args):
        if any([type(arg) is float for arg in args]):
            return float
        return int

