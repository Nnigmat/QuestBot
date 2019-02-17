class Circular_Buffer:

    def __init__(self, array):
        self.array = array
        self.counter = 0
        self.lenght = len(array)

    def create_client(self, chat_id):
        client = Client(start=self.counter, end=Client.prev_position(self.counter, self.lenght - 1), buf=self, chat_id=chat_id)
        print(self.counter,Client.prev_position(self.counter, self.lenght - 1), chat_id)
        self.counter = Client.next_position(self.counter, self.lenght - 1)
        return client
    
    def get(self, index):
        return self.array[index]


class Client:

    def __init__(self, start, end, buf, chat_id):
        self.start = start
        self.current = start
        self.end = end
        self.passed = 0
        self.buf = buf
        self.chat_id = chat_id
        self.help = True

    def get_type(self):
        return self.buf.get(self.current)['type']

    def get_current(self):
        return self.buf.get(self.current)['current']

    def get_next(self):
        return self.buf.get(self.current)['next']

    def get_text(self):
        return self.buf.get(self.current)['text']

    def answer(self, answer):
        if not self.is_ended():
            if self.get_next() == answer:
                self.shift()
                return True
            else:
                return False
        else:
            return None

    def shift(self):
        self.current = Client.next_position(self.current, self.buf.lenght - 1)
        self.passed += 1

    def is_ended(self):
        return self.passed == self.buf.lenght - 1

    def get_help(self):
        if self.help:
            self.help = False
            return True
        else:
            return False

    @staticmethod
    def next_position(current, length):
        return current + 1 if current + 1 <= length else 0

    @staticmethod
    def prev_position(current, length):
        return current - 1 if current - 1 >= 0 else length