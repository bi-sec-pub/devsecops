import ssl
import urllib.error
import urllib.parse
import urllib.request
import http.client as httplib
import base64


def runManualAutomationTemplate(curr_url, post_data, expected_responseText):
    global errorcount, bauth_string
    ctx = ssl.create_default_context()
    ctx.check_hostname = True  # change for testing environment
    ctx.verify_mode = ssl.CERT_REQUIRED

    try:
        req = urllib.request.Request(url=curr_url)

        req.add_header("Authorization", "Basic %s" % bauth_string)
        result = urllib.request.urlopen(url=req, data=post_data, context=ctx)
        resp = result.read().decode('utf-8')
        respheader = result.headers
        # uncomment for debug / info
        # print(respheader)
        # print(resp)
        # print(result.getcode())
        if resp.find(expected_responseText) > 0:
            print("Warning: Expected text found")
            errorcount += 1
        elif result.getcode() == 302:
            print("Redirect detected")
            # Deal with it
        else:
            print("Error: Expected text missing")
            # Deal with it

    except urllib.error.URLError as e:
        print("URLError ", e)
    except IOError as i:
        print("IOError ", i)
    except httplib.BadStatusLine as x:
        print("BadStatusLine ", x)
    except httplib.IncompleteRead as he:
        print("IncompleteRead ", he)
    except httplib.HTTPException as gen_err:
        print("GenErr ", gen_err)
    pass
    return 0

def get_bauth_string(auth_user: str, auth_pass: str) -> bytes:
    return base64.b64encode(('%s:%s' % (auth_user, auth_pass)).encode('utf-8'))

curr_url = "https://lab.bi-sec.de"
errorcount = 0
bauth_string = get_bauth_string("dummy", "dummy")

# Test case #1
post_data = urllib.parse.urlencode({'username': "testusr", 'password': "testpw", 'captcha': 'testcaptcha', 'send': 'Login'}).encode('utf-8')
expected_text = "Wrong username"
runManualAutomationTemplate(curr_url, post_data, expected_text)

# Test case #2
post_data = urllib.parse.urlencode({'username': "admin", 'password': "testpw", 'captcha': 'testcaptcha', 'send': 'Login'}).encode('utf-8')
expected_text = "Wrong password"
runManualAutomationTemplate(curr_url, post_data, expected_text)

# Test case #3
post_data = urllib.parse.urlencode({'username': "admin", 'password': "admin", 'captcha': 'testcaptcha', 'send': 'Login'}).encode('utf-8')
expected_text = "Invalid captcha"
runManualAutomationTemplate(curr_url, post_data, expected_text)

# Test case #4
post_data = urllib.parse.urlencode({'username': 'admin', 'password': 'admin', 'captcha': '7', 'send': 'Login'}).encode('utf-8')
expected_text = "Anmeldung bi-sec lab"
runManualAutomationTemplate(curr_url, post_data, expected_text)

print("Test completed. Problematic responses: " + str(errorcount))
