import json

class AWXClientRequestException(Exception):
    def __init__(self, status='', message=''):
        if isinstance(status, Exception):
            self.status = ''
            return super(AWXClientRequestException, self).__init__(*status)
        self.status = status
        self.msg = json.dumps(message)

    def __getitem__(self, val):
        return (self.status, self.msg)[val]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '{} - {}'.format(self.status, self.msg)
