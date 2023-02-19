
from threading import Event

if __name__ == '__main__':

    delay = 5        # 秒

    print('Go to sleep…')
    Event().wait(delay)
    print('Back to work…')
