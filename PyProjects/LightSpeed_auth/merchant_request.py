import requests
from Token import _get_access_token, _ACCOUNT_ID
from tkinter import *
import xml.etree.ElementTree as etree


def get_request(request_string):
    i = 1
    while True:
        request_call= 'https://api.merchantos.com/API/Account/%s/Item/%s?load_relations=["ItemShops"]'%(_ACCOUNT_ID(),
                                                                    i)
        payload = {"authorization": 'Bearer %s' %(_get_access_token()) }
        response = requests.get( request_call, headers=payload)
        if response.status_code != 200:
            break
        root = etree.fromstring(response.text)

        print(root.findall('Prices')[0][0][0].text) # THis will show the default price

        # for test in root.findall('Prices')[0][0]:
        #     print(test.text)

        #print(root[26][1][0].text)
        # for child in root:
        #     print(child.tag)
        for child in root:
            print(child.tag + ': ' , root.findall(child.tag)[0].text)
        print ("----------------------------------------------------\n")
        i += 1




#-----------------------MAIN CODE--------------------------------------
#
# OPTIONS = [
# "Category",
# "Item",
# "Workorder"
# ] #etc
#
# master = Tk()
#
# variable = StringVar(master)
# variable.set(OPTIONS[0]) # default value
#
# w = OptionMenu(master, variable, *OPTIONS)
# w.pack()
#
# def ok():
#     get_request(variable.get())
#     exit()
#
# button = Button(master, text="OK", command=ok)
# button.pack()
#
# mainloop()


get_request('Item')
