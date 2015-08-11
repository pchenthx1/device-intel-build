#!/usr/bin/env python


class IniParser:

    def __init__(self):
        self.sec = {'DEFAULT': {}}
        self.cursec = self.sec['DEFAULT']
        # We need to have the ordered list of sections
        # so that command sets will be executed in the order of the .ini
        self.seclist = []

    def fix_type(self, s):
        if s.lower() == 'true':
            return True
        if s.lower() == 'false':
            return False
        if s.isdigit():
            return int(s)
        return s

    def new_section(self, line):
        section = line[1:len(line) - 1]
        if section not in self.sec:
            self.sec[section] = {}
            self.seclist.append(section)
        self.cursec = self.sec[section]

    def append_option(self, option, data):
        option = option.strip()
        data = data.strip()
        if option in self.cursec:
            self.cursec[option] = ' '.join([self.cursec[option], data])
        else:
            self.cursec[option] = data

    def new_option(self, line):
        option, data = line.split('=', 1)
        if option[-1] == '+':
            self.append_option(option[:-1], data)
            return

        option = option.strip()
        data = data.strip()
        self.cursec[option] = self.fix_type(data)

    def parse(self, f):
        for line in f:
            l = line.strip()
            if l.startswith('[') and l.endswith(']'):
                self.new_section(l)
                continue
            if not l:
                continue
            if l.startswith('#') or l.startswith(';'):
                continue
            if l.find('=') > 1:
                self.new_option(l)
                continue
            raise Exception('INI Parsing error, offending line is ' + l)

    def sectionsfilter(self, start):
        return [(s, s[len(start):])
                for s in self.seclist if s.startswith(start)]

    def sections(self):
        return self.seclist

    def options(self, section):
        return self.sec[section].keys()

    def has_option(self, section, option):
        if section not in self.sec:
            return False
        if option in self.sec[section]:
            return True
        return False

    def get(self, section, option):
        return self.sec[section][option]

    def copy_option(self, section, opt_list):
        option = {}
        for opt in opt_list:
            if self.has_option(section, opt):
                option[opt] = self.get(section, opt)
        return option
