import os
import re
import shutil
import datetime

pic_dir = '.'

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

pic_files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(pic_dir):
    for filename in f:
        main_name, ext = split_last(filename.lower(), os.path.extsep)
        if ext in ['jpg', 'jpeg']:
            pic_files.append(filename)
pic_files.sort()

def split_str_num(str_in):
    temp = re.compile('([a-zA-Z]+)([0-9]+)') 
    return temp.match(str_in).groups() 

def append_num_suffix(day):
    num_suffix = ['th', 'st', 'nd', 'rd']
    if day % 10 in [1, 2, 3] and day not in [11, 12, 13]:
        return str(day) + num_suffix[day % 10]
    else:
        return str(day) + num_suffix[0]

def filename_to_date_string(name_in):
    main_name, ext = split_last(name_in.lower(), os.path.extsep)

    year, month, dayrem = main_name.split('-')
    if '_' in dayrem:
        day, rem = dayrem.split('_')
    else:
        day = dayrem
        rem = None
    
    year = int(year)
    month = int(month)
    day = int(day)
    
    date = datetime.date(year=year, month=month, day=day)
    
    final_name = date.strftime('%A %B') + ' '
    final_name += append_num_suffix(date.day) + ' '
    final_name += date.strftime('%Y')
    #final_name += ', Page # Unknown'
    if rem != None:
        final_name += ', Comment: ' + rem
    return final_name

def main():
    strings = []
    for f in pic_files:
        these_strings = dict()
        these_strings['date'] = filename_to_date_string(f)
        these_strings['title'] = '## ' + these_strings['date'] + ' [[Table of Contents](#table-of-contents)]'
        these_strings['pic'] = '![' + these_strings['date'] + '](' + f + ')'
        these_strings['link'] = '#' + these_strings['date'].lower().replace(',', '').replace(':', '').replace(' ', '-') + '-table-of-contents'
        strings.append(these_strings)
    
    print('## Table of Contents')
    for s in strings:
        print('* [' + s['date'] + '](' + s['link'] + ')')
    print('\n')
    for s in strings:
        print(s['title'])
        print(s['pic'])
main()
