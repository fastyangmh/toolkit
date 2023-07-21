#import
import sys


#def
def get_os_name():
    os_name_table = {
        'darwin': 'macOS',
        'linux': 'Linux',
        'win32': 'Microsoft Windows'
    }
    platform = sys.platform
    os_name = os_name_table[platform]
    return os_name


if __name__ == '__main__':
    #run
    os_name = get_os_name()
    print(os_name)