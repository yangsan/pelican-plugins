# -*- coding: utf8 -*-
import markdown
import re
import subprocess
import os


class InsertCodePreprocessor(markdown.preprocessors.Preprocessor):
    def __init__(self, settings):
        self.settings = settings

        self.replacement = [
            ("insertcodehere \w+\.py", self.replaceWithCode),
            ("insertresulthere \w+\.py", self.replaceWithResult)
        ]

        if self.settings and "path" in self.settings:
            path = self.settings["path"]
        else:
            path = "./content/code/"

        if path[-1] == "/":
            self.pwd = path
        else:
            self.pwd = path + "/"

        self.list_of_code_files = os.listdir(self.pwd)

    def run(self, content):
        # @param content: a list of unicode string of the entire file and each
        # string contain one line of text
        # @return: a list of strings

        # find and replace the insert line
        for i, line in enumerate(content):
            for pattern, func in self.replacement:
                if isinstance(line, unicode) and\
                        re.match(pattern, line):
                    content[i] = func(line)

        return self._flatten(content)

    def _flatten(self, the_list):
        # helper function, flatten the list
        # @param: the_list, a list contain only strings and list of strings
        # @return: a list of all the string in the_list
        flatten_list = []
        for item in the_list:
            if isinstance(item, list):
                for string in item:
                    flatten_list.append(string)
            else:
                flatten_list.append(item)
        return flatten_list

    def replaceWithCode(self, line):
        # @param line: a line of text to be replaced
        # @return: a list of parsed code string, each string contain a line of code
        code_file_name = line.strip().split()[1]

        if code_file_name not in self.list_of_code_files:
            return "No such file as '%s'" % code_file_name

        with open(self.pwd + "/" + code_file_name, "r") as f:
            codes = f.read().split("\n")


        #parsed_code = ["".join(["    ", line.decode("utf8")]) for line in codes[1:]]
        parsed_code = self._prependTab(codes[1:])

        return [u'    :::python\n'] + parsed_code

    def replaceWithResult(self, line):
        # @param file_name: the file name of wanted python script
        # @return: a list of result of running the python script
        code_file_name = line.strip().split()[1]

        if code_file_name not in self.list_of_code_files:
            return "No such file as '%s'" % code_file_name

        file_name = self.pwd + "/" + code_file_name
        result = subprocess.check_output(["python", file_name],
                                         stderr=subprocess.STDOUT)

        parsed_result = self._prependTab(result.split("\n"))

        return parsed_result


    def _prependTab(self, list_of_strings):
        # helper function: preappend a tab to every line of list_of_string
        # @param list_of_string: a list of strings
        # @return: a list of strings with tab in front of it
        tab = "    "
        return ["".join([tab, line.decode("utf8")]) for line in list_of_strings]

class InsertCodeExtansion(markdown.Extension):
    def __init__(self, settings):
        self.settings = settings

    def extendMarkdown(self, md, md_globals):
        #print "Add extension to md"
        md.preprocessors.add("insert", InsertCodePreprocessor(self.settings), ">reference")

if __name__ == "__main__":
    pass
