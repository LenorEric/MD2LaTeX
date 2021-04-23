import re

if __name__ == '__main__':
    if re.match('[1-9]+\.', '12a.'):
        print(re.match('[1-9]+\.', '12a.'))
