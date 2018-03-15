import requests
import time
class request_management:
    def create_new_session(self):
        self.sess = requests.Session()
        self.sess.headers.update ({
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Referrer" : "http://legacy.hackerexperience.com"
        })

    def get_request(self, url, max_attempts, delay):
        response = self.sess.get(url)
        while max_attempts > 0:
            if response.status_code == 200:
                return(response)
            else:
                print("Request Failed.")
                print("Retrying...")
                max_attempts = max_attempts - 1
                print(max_attempts)
                time.sleep(delay)
        return(False)

    def check_if_logged_in(self):
        url = "http://legacy.hackerexperience.com"
        web_resp = self.get_request(url,10,3)
        if(web_resp != False):
            if "Hacker Experience is a browser-based hacking simulation game" in web_resp.text:
                return(True)
            else:
                return(False)
        else:
            return(False)

request = request_management()
request.create_new_session()
print(request.check_if_logged_in())
