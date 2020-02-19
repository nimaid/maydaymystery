import os
import re
import shutil

unsorted_dir = 'unsorted'

unsorted_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(unsorted_dir):
    for file in f:
        unsorted_files.append(file)

def split_last(str_in, sep, first=False):
    separated = str_in.split(sep)
    if first:
        end = sep.join(separated[1:])
        first = separated[0]
        return first, end
    else:
        start = sep.join(separated[:-1])
        last = separated[-1]
        return start, last

def split_str_num(str_in):
    temp = re.compile("([a-zA-Z]+)([0-9]+)") 
    return temp.match(str_in).groups() 

def name_to_date(name_in):
    main_name, ext = split_last(name_in.lower(), os.path.extsep)
    if ext not in ['jpg', 'gif']:
        raise ValueError('Is not a gif or jpg!')

    year, monthday = split_last(main_name, '-', first=True)
    if monthday == '':
        year, monthday = split_last(main_name, '_', first=True)
    if monthday == '':
        raise ValueError('Invalid format!')
    if int(year) > 50:
        year = '19' + year
    else:
        year = '20' + year
    
    month_names = { '1': ['jan'],
                    '2': ['feb'],
                    '3': ['mar'],
                    '4': ['apr', 'april'],
                    '5': ['may'],
                    '6': ['jun', 'june'],
                    '7': ['jul', 'july'],
                    '8': ['aug'],
                    '9': ['sept', 'sep'],
                    '10': ['oct'],
                    '11': ['nov'],
                    '12': ['dec'] }
    
    monthname, day = split_str_num(monthday)
    remainder = monthday[len(monthname) + len(day):]

    month = None
    for x in range(1, 13):
        if monthname in month_names[str(x)]:
            month = x
            break
    if month == None:
        raise ValueError('Invalid month name {}!'.format(monthname))

    final_name = year + '-' + str(month) + '-' + day
    if remainder != '':
        final_name += '_' + remainder[1:]
    final_name += os.path.extsep + ext
    return final_name

def main():
    for file in unsorted_files:
        src_path = os.path.join(unsorted_dir, file)
        dest_path = name_to_date(file)
        print('{} => {}'.format(src_path, dest_path))
        shutil.copyfile(src_path, dest_path)
