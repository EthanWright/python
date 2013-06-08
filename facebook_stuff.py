import pycurl
import re
from cStringIO import StringIO

username = ''
email = ''

def parse_cookie(buffer):
    cookie = ''
    results = re.search("c_user=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 'c_user=' + results.group(1) + ';'
    results = re.search("csm=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 'csm=' + results.group(1) + ';'
    results = re.search("datr=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 'datr=' + results.group(1) + ';'
    results = re.search("fr=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 'fr=' + results.group(1) + ';'
    results = re.search("lu=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 'lu=' + results.group(1) + ';'
    results = re.search("s=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 's=' + results.group(1) + ';'
    results = re.search("xs=(.*); expires", buffer)
    if results is not None:
        cookie = cookie + 'xs=' + results.group(1) + ';'
    return cookie

def post_status(cookie, fb_dtsg):
    posts="""fb_dtsg:%s
xhpc_context:home
xhpc_ismeta:1
xhpc_timeline:
xhpc_composerid:u_jsonp_4_0
xhpc_targetid:eb4c6d1a60e19a7795da501e1f468035
xhpc_message_text:
xhpc_message:sup dude
is_explicit_place:yes
composertags_place:france
composertags_place_name:
composer_session_id:1366058826
action_type_id[0]:383634705006159
object_str[0]:
object_id[0]:
composertags_city:
disable_location_sharing:false
composer_predicted_city:
audience[0][value]:10
nctr[_mod]:pagelet_composer
__user:663553091
__a:1
__dyn:798aD5yJpGvzaEa0
__req:r
phstamp:165816710910610667102476""" % fb_dtsg
    posts = posts.replace("\n","&")
    posts = posts.replace(":","=")
    buffer = StringIO()
    buffer2 = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.facebook.com/ajax/updatestatus.php')
    c.setopt(c.REFERER, 'https://www.facebook.com/')
    #c.setopt(c.USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22')
    c.setopt(c.POSTFIELDS, posts)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.setopt(c.HEADERFUNCTION, buffer2.write)
    c.setopt(c.COOKIE, cookie)
    c.perform()

    print buffer2.getvalue()

def login(cookie):
    posts = 'lsd=AVpGKS80&email=%s&pass=%s&persistent=1&default_persistent=1&timezone=420&lgnrnd=113628_R444&lgnjs=1366050987&locale=en_US' % (email, password)
    buffer = StringIO()
    buffer2 = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.facebook.com/login.php?login_attempt=1')
    c.setopt(c.REFERER, 'https://www.facebook.com/')
    c.setopt(c.COOKIE, cookie)
    #c.setopt(c.USERAGENT, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22')
    c.setopt(c.POSTFIELDS, posts)
    c.setopt(c.HEADERFUNCTION, buffer2.write)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()
    print buffer2.getvalue()
    return parse_cookie(buffer2.getvalue())


def get_stuff(logged_in, cookie):
    buffer = StringIO()
    buffer2 = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.facebook.com/')
    if logged_in == 1:
        c.setopt(c.COOKIE, cookie)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.setopt(c.HEADERFUNCTION, buffer2.write)
    c.perform()

    print buffer2.getvalue()
    if logged_in == 1:
        fb_dtsg = re.search("name=\"fb_dtsg\" value=\"([0-9a-zA-Z]{8})\"", buffer.getvalue()).group(1)
        return fb_dtsg
    else:
        cookie = parse_cookie(buffer2.getvalue())
        return cookie

def main():

    cookie = get_stuff(0, '')
    cookie = login(cookie)
    fb_dtsg = get_stuff(1, cookie)
    post_status(cookie, fb_dtsg)

if __name__ == '__main__':
    main()







"""
fb_dtsg=AQDPboLf&xhpc_context=home&xhpc_ismeta=1&xhpc_timeline=&xhpc_composerid=u_0_g&xhpc_targetid=663553091&icon_id=&xhpc_message_text=sup&xhpc_message=sup&is_explicit_place=&composertags_place=&composertags_place_name=&composer_session_id=1365558941&action_type_id[0]=383634705006159&object_str[0]=ham&object_id[0]=&composertags_city=&disable_location_sharing=false&composer_predicted_city=114952118516947&audience[0][value]=10&nctr[_mod]=pagelet_composer&__user=663553091&__a=1&__dyn=798aD5yJpGvzaEa0&__req=k&phstamp=1658168809811176102512


fb_dtsg:AQCmjjCf
xhpc_context:home
xhpc_ismeta:1
xhpc_timeline:
xhpc_composerid:u_jsonp_2_0
xhpc_targetid:663553091
xhpc_message_text:hi there
xhpc_message:hi there
is_explicit_place:
composertags_place:
composertags_place_name:
composer_session_id:1366055832
action_type_id[0]:
object_str[0]:
object_id[0]:
composertags_city:
disable_location_sharing:false
composer_predicted_city:
audience[0][value]:10
nctr[_mod]:pagelet_composer
__user:663553091
__a:1
__dyn:798aD5yJpGvzaEa0
__req:j
phstamp:165816710910610667102490

fb_dtsg:AQD9Gxy_
xhpc_context:home
xhpc_ismeta:1
xhpc_timeline:
xhpc_composerid:u_0_g
xhpc_targetid:663553091
xhpc_message_text:I lit something on fire for the first time in like a month. For some reason I am very disappointed to have had that long a lull.
xhpc_message:I lit something on fire for the first time in like a month. For some reason I am very disappointed to have had that long a lull.
is_explicit_place:
composertags_place:
composertags_place_name:
composer_session_id:1366085116
action_type_id[0]:
object_str[0]:
object_id[0]:
composertags_city:
disable_location_sharing:false
composer_predicted_city:114952118516947
audience[0][friends]:30
audience[0][lists][0]:10151410276093092
audience[0][_pr_]:1366085160
audience[0][custom_value]:111
audience[0][value]:111
nctr[_mod]:pagelet_composer
__user:663553091
__a:1
__dyn:798aD5yJpGvzaEa0
__req:o
phstamp:1658168577112012195963
Response Headersview source

"""
