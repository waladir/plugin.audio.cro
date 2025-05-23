# -*- coding: utf-8 -*-
import xbmcgui
import xbmcaddon

import codecs
import json

from libs.utils import call_api, get_userdata_dir

addon = xbmcaddon.Addon(id='plugin.audio.cro')

def get_person(personId):
    filename = get_userdata_dir() + "persons.txt"
    
    persons = get_persons()
    if personId in persons.keys():
        return persons[personId]
    else:
        data = call_api(url = "https://api.mujrozhlas.cz/persons/" + personId)
        if "err" not in data and "data" in data and len(data["data"]) > 0 and "attributes" in data["data"] and "title" in data["data"]["attributes"] and len(data["data"]["attributes"]["title"]) > 0:
            title = data["data"]["attributes"]["title"]
            persons.update({ personId : title })
            try:
                with codecs.open(filename, "w", encoding="utf-8") as file:
                    data = json.dumps(persons)
                    file.write('%s\n' % data)
            except IOError:
                xbmcgui.Dialog().notification("ČRo","Problém při osob", xbmcgui.NOTIFICATION_ERROR, 4000)
            return title
        else:
            return ""

def get_persons():
    persons = {}
    filename = get_userdata_dir() + "persons.txt"
    try:
      with codecs.open(filename, "r", encoding="utf-8") as file:
        for line in file:
          item = line[:-1]
          persons = json.loads(item)
    except IOError:
      pass
    return persons
