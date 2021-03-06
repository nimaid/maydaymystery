#!/usr/bin/env python3
import os
import sys
import datetime

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
    
    final_name = date.strftime('%Y %B') + ' '
    final_name += append_num_suffix(date.day) + ' '
    final_name += date.strftime('(%A)')

    if rem != None:
        final_name += ' {' + rem + '}'
    return final_name

def main(pic_dir):
    pic_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(pic_dir):
        for filename in f:
            main_name, ext = split_last(filename.lower(), os.path.extsep)
            if ext in ['jpg', 'jpeg']:
                pic_files.append(filename)
        break #prevent descending into subfolders
    pic_files.sort()

    strings = []
    for f in pic_files:
        these_strings = dict()
        these_strings['date'] = filename_to_date_string(f)
        these_strings['title'] = '## ' + these_strings['date'] + ' [[Table of Contents]](#table-of-contents)'
        these_strings['pic'] = '![' + these_strings['date'] + '](' + f + ')'
        
        these_strings['link'] = these_strings['date'].lower()
        for x in ',()[]{}#':
            these_strings['link'] = these_strings['link'].replace(x, '')
        these_strings['link'] = these_strings['link'].replace(' ', '-')
        these_strings['link'] += '-table-of-contents'
        these_strings['link'] = '#' + these_strings['link']
        strings.append(these_strings)
    
    print('## Table of Contents')
    for s in strings:
        print('* [' + s['date'] + '](' + s['link'] + ')')
    print('\n')
    for s in strings:
        print(s['title'])
        print('<details>')
        print('  <summary>Show</summary>')
        print()
        print('  ' + s['pic'])
        print('</details>')
        print()

script_path = os.path.dirname(os.path.realpath(__file__))
main(script_path)
