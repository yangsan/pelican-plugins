# -*- coding: utf8 -*-
import pelican
from .insertcodemdextention import InsertCodeExtansion


def addMdExtention(pelicanobj):
    #print issubclass(InsertCodeExtansion, markdown.Extension)
    try:
        insert_code_setting = pelicanobj.settings["INSERT_CODE"]
    except:
        insert_code_setting = None

    #print insert_code_setting

    pelicanobj.settings["MD_EXTENSIONS"].append(InsertCodeExtansion(insert_code_setting))


def register():
    pelican.signals.initialized.connect(addMdExtention)
