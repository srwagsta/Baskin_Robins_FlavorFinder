from urllib import request, parse
from xml.etree import ElementTree as etree

#reddit parse
wired_file = request.urlopen('https://www.wired.com/feed/rss')
#convert to string:
wired_data = wired_file.read()
#close file because we dont need it anymore:
wired_file.close()

#entire feed
wired_root = etree.fromstring(wired_data)
item = wired_root.findall('channel/item')

for entry in item:
    fname = '<p>' + entry.findtext('title') + '</p>'
    lname = 'Published on: ' + entry.findtext('pubDate')
    email = '<a href="' + entry.findtext('link') + '">View this page!!</a>'
    comment = '<h2>' + entry.findtext('description') + '</h2>'
    data = {
                'fname': fname,
                'lname': lname,
                'email': email,
                'comment': comment
               }
    encoded_data = parse.urlencode(data).encode()
    req = request.Request("http://infost440.uwmsois.com/week8/assignment8/comment.php",encoded_data)
    print(request.urlopen(req))


#
# for x in range(0,100):
#     guestbook_id = x
#     data = {
#                 'guestbook_id': guestbook_id
#
#                }
#     encoded_data = parse.urlencode(data).encode()
#     req = request.Request("http://infost440.uwmsois.com/week8/assignment8/delete.php",encoded_data)
#     print(request.urlopen(req))
