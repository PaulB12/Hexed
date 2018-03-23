import requests
import time
from datetime import datetime
class requestManage:
    def create_new_session(self):
        initalised = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Initilizating a new request session @ "+initalised)
        self.sess = requests.Session()
        self.sess.headers.update ({
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Referrer" : "http://legacy.hackerexperience.com"
        })
        self.sess.cookies.update({
            'PHPSESSID':'te75e230ekqmucsnkil06ib1o1'
        })

        print("OK!")

    def get_request(self, url, max_attempts, delay, status):
        if (status != 1):
            if(self.check_if_logged_in()):
                while max_attempts > 0:
                    response = self.sess.get(url)
                    if response.status_code == 200:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        self.url_log(url, "GET", str(max_attempts), str(delay), " ", current_time, "1")
                        return(response)
                    elif response.status_code == 502:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("Hacker Experience Cloudflare Error @ "+current_time)
                        time.sleep(3)
                    elif response.status_code == 302 or response.status_code == 301:
                        if response.text == "":
                            print("Our PHPSESSID has been blocked! Resetting. BOT needs to relog!")
                            self.create_new_session()
                    else:
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        self.url_log(self, url, "GET", str(max_attempts), str(delay), " ", current_time, "0")
                        print("GET Request Failed for "+url+" at "+current_time)
                        print("Retrying after "+delay+" seconds.")
                        max_attempts = max_attempts - 1
                        time.sleep(delay)
                return(False)
            else:
                return(False)
        else:
            while max_attempts > 0:
                response = self.sess.get(url)
                if response.status_code == 200:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.url_log(url, "GET", str(max_attempts), str(delay), " ", current_time, "1")
                    return(response)
                elif response.status_code == 502:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print("Hacker Experience Cloudflare Error @ "+current_time)
                    time.sleep(3)
                elif response.status_code == 302 or response.status_code == 301:
                    if response.text == "":
                        print("Our PHPSESSID has been blocked! Resetting. BOT needs to relog!")
                        self.create_new_session()
                else:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.url_log(self, url, "GET", str(max_attempts), str(delay), " ", current_time, "0")
                    print("GET Request Failed for "+url+" at "+current_time)
                    print("Retrying after "+delay+" seconds.")
                    max_attempts = max_attempts - 1
                    time.sleep(delay)
            return(False)



    def post_request(self, url, payload, max_attempts, delay):
        if(self.check_if_logged_in()):
            while max_attempts > 0:
                response = self.sess.post(url,payload)
                if response.status_code == 200:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.url_log(url, "POST", str(max_attempts), str(delay), str(payload), str(current_time), "1")
                    return(response)
                elif response.status_code == 502:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print("Hacker Experience Cloudflare Error @ "+current_time)
                    time.sleep(3)
                elif response.status_code == 302 or response.status_code == 301:
                    if response.text == "":
                        print("Our PHPSESSID has been blocked! Resetting. BOT needs to relog!")
                        self.create_new_session()
                else:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.url_log(self, url, "POST", str(max_attempts), str(delay), str(payload), str(current_time), "0")
                    print("POST Request Failed for "+url+" at "+current_time)
                    print("Retrying after "+delay+" seconds.")
                    max_attempts = max_attempts - 1
                    time.sleep(delay)
            return(False)
        else:
            return(False)

    def check_if_logged_in(self):
        url = "http://legacy.hackerexperience.com"
        web_resp = self.get_request(url,10,3,1)
        if(web_resp != False):
            if "Hacker Experience is a browser-based hacking simulation game" in web_resp.text or "not logged in" in web_resp.text:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("We're logged out at "+current_time)
                #Log me back in!
                return(False)
            else:
                return(True)
        else:
            return(False)

    def save_data(self,path,data):
        with open(path,"a") as file:
            file.writelines(data)

    def url_log(self,url,type,max_attempts,delay,val1,val2,val3):
        data = url+";,;"+type+";,;"+max_attempts+";,;"+delay+";,;"+val1+";,;"+val2+";,;"+val3+"\n"
        self.save_data("logs/request_log.txt",data)
