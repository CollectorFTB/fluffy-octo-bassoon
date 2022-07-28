import time

from driver import init_session, close_session
from poe import search_item

def main():
    
    search_item('Grace', **{'Corrupted': 'No', 'Mirrored': 'No', 'Quality': (1,10)})
    #@search_item('''Shavronne's Wrappings Occultist's Vestment''')



if __name__ == '__main__':
    try:
        init_session()
        main()
    finally:
        close_session()
