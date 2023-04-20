#!/usr/bin/env python

def color(str,str_color):

                        #string attributes and foreground color

    colors = {
            'reset':'\033[00m',
            'bold':'\033[01m',
            'disable':'\033[02m',
            'underline':'\033[04m',
            'reverse':'\033[07m',
            'strikethrough':'\033[09m',
            'invisible':'\033[08m',
            'black':'\033[30m',
            'red':'\033[31m',
            'green':'\033[32m',
            'orange':'\033[33m',
            'blue':'\033[34m',
            'purple':'\033[35m',
            'cyan':'\033[36m',
            'lightgrey':'\033[37m',
            'darkgrey':'\033[90m',
            'lightred':'\033[91m',
            'lightgreen':'\033[92m',
            'yellow':'\033[93m',
            'lightblue':'\033[94m',
            'pink':'\033[95m',
            'lightcyan':'\033[96m'
    }

                    #background color

    # colors_bg = {
    #     'black':'\033[40m',
    #     'red':'\033[41m',
    #     'green':'\033[42m',
    #     'orange':'\033[43m',
    #     'blue':'\033[44m',
    #     'purple':'\033[45m',
    #     'cyan':'\033[46m',
    #     'lightgrey':'\033[47m'
    #     }

    str_color=colors[str_color]

    return str_color+str+colors['reset']
