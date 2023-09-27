
class RequestException(Exception):
    """ RequestException """

    def __init__(self, *args):
        super().__init__(*args)

    def __str__(self):
        return self.__doc__ + '\n' + super().__str__()