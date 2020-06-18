import re
import requests

from credentials import Credentials

url_base = 'https://www.facebook.com'


def post_status(status, cookies, fb_dtsg):
    params = {
        'fb_dtsg': fb_dtsg,
        'xhpc_context': 'home',
        'xhpc_ismeta': 1,
        'xhpc_timeline': None,
        'xhpc_composerid': 'u_jsonp_4_0',
        'xhpc_targetid': 'eb4c6d1a60e19a7795da501e1f468035',
        'xhpc_message_text': status,
        'xhpc_message': status,
        'is_explicit_place': 'yes',
        'composertags_place': 'france',
        'composertags_place_name': None,
        'composer_session_id': '1366058826',
        'action_type_id[0]': '383634705006159',
        'object_str[0]': None,
        'object_id[0]': None,
        'composertags_city': None,
        'disable_location_sharing': 'false',
        'composer_predicted_city': None,
        'audience[0][value]': 10,
        'nctr[_mod]': 'pagelet_composer',
        '__user': '663553091',
        '__a': 1,
        '__dyn': '798aD5yJpGvzaEa0',
        '__req': 'r',
        'phstamp': '165816710910610667102476',
    }
    headers = {
        'referer': url_base,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22',
    }
    api_endpoint = 'ajax/updatestatus.php'
    response = requests.post(
        requests.compat.urljoin(url_base, api_endpoint),
        cookies=cookies,
        headers=headers,
        data=requests.compat.urlencode(params)
    )
    body = response.text
    response.close()
    return


def parse_cookies(response_cookies):
    split_cookies = response_cookies.split(', ')

    cookies = {}
    for data in split_cookies:
        search_results = re.match('([a-zA-Z]*)=(.*); expires', data)
        if search_results:
            cookies[search_results.group(1)] = search_results.group(2)

    return cookies


def get_fb_dtsg(cookies):
    response = requests.get(url_base, cookies=cookies)
    body = response.text
    response.close()
    fb_dtsg = re.search('name="fb_dtsg" value="([0-9a-zA-Z]{8})"', body)
    if fb_dtsg:
        return fb_dtsg.group(1)


def get_cookies():
    response = requests.get(url_base)
    headers = response.headers
    response.close()

    return parse_cookies(headers.get('Set-Cookie'))


def login(cookies):
    credentials = Credentials('facebook')
    params = {
        'lsd': 'AVpGKS80',
        'email': credentials.get('email'),
        'pass': credentials.get('pass'),
        'persistent': '1',
        'default_persistent': '1',
        'timezone': '420',
        'lgnrnd': '113628_R444',
        'lgnjs': '1366050987',
        'locale': 'en_US',
        'login_attempt': 1,
    }
    api_endpoint = 'login.php'
    url = requests.compat.urljoin(url_base, api_endpoint)
    response = requests.post(url, params=params, cookies=cookies)
    headers = response.headers
    response.close()

    return parse_cookies(headers.get('Set-Cookie'))


def run():

    cookies = get_cookies()
    cookies = login(cookies)
    fb_dtsg = get_fb_dtsg(cookies)
    status = 'test status'
    post_status(status, cookies, fb_dtsg)


if __name__ == '__main__':
    run()