from multiprocessing.dummy import Pool as ThreadPool
import request_management
import re
import time
from bs4 import BeautifulSoup
class game_info:
    def __init__(self, request_starter):
        print("Initalizating game_info class...")
        self.request = request_starter
        print("OK!")

    def grab_local_log(self):
        web_resp = self.request.get_request("https://legacy.hackerexperience.com/log",3,5,0)
        try:
            soup = BeautifulSoup(web_resp.text, 'html.parser')
            Log = soup.find('textarea', {'name': 'log'})
            return(Log.text)
        except:
            return(False)

    def parse_log(self,log):
        regex = r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
        matches = re.findall(regex, log)
        if(len(matches) == 0):
            return(False)
        else:
            return(matches)

    def wipe_local_log(self):
        url = "https://legacy.hackerexperience.com/logEdit"
        payload = {
            'id':'1',
            'log':'',
        }
        if((self.request.post_request(url,payload,5,10)) != False):
            return(True)
        else:
            return(False)

    def fetch_active_process(self):
        url = "https://legacy.hackerexperience.com/processes"
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):
            if('<script type="text/javascript">' in web_resp.text):
                js = web_resp.text.split('var iNow=new Date()')[1].split('</script>')[0].split("new Date().getTime()+")
                proc_id = list()
                time_left = list()
                proc_completed = list()
                for proc in js:
                    if '*1000' in proc:
                        time_left.append(proc.split('*1000')[0])
                        data = proc.split('finish:iEnd,interval:100,id:')[1]
                        #print(data)
                        proc_id.append(data.split(",")[0])
                        proc_completed.append(data.split("loaded:")[1].split("}")[0])
                print(proc_id)
                print(time_left)
                print(proc_completed)
                proc_html = BeautifulSoup(web_resp.text, 'html.parser')
                for each in proc_id:
                    pr_cl = "span4 processBlock"+proc_id
                    proc_desc = proc_html.find('div', {'class': pr_cl}).find('div',{'class':'proc-desc'}).text
                print(proc_desc)
                return(True)
            else:
                return(False)
        else:
            return(False)
    def grab_local_software_ids_folder_bug(self):
        url = "https://legacy.hackerexperience.com/software"
        web_resp = self.request.get_request(url, 3, 5, 0)
        folder = list()
        if(web_resp != False):

            soup = BeautifulSoup(web_resp.text, 'html.parser')
            proc = soup.find('div', {'class':'span9'})
            regex = r'id\=\"[\d]+\"'
            matches = re.findall(regex, str(proc))
            folder = list()
            software = list()
            for procid in matches:
                procid = procid.split('id="')[1].split('"')[0]
                proc2 = str(proc.find('tr', {'id':str(procid)}))
                if 'Folder' in proc2:
                    folder.append(procid)
                else:
                    software.append(procid)
            return (software, folder[0])
        else:
            return(False)

    def move_to_folder(self,software,folder_id):
        url = "https://legacy.hackerexperience.com/software"
        threads = list()
        ac_py = list()
        for soft_id in software:
            payload = {
                'action':'folder',
                'view':folder_id,
                'id':soft_id,
                'act':'move-folder',
            }
            ac_py.append(payload)
        return(ac_py)
    def send_post_folder(self,payload):
        Check = 3
        while Check > 0:
            response = self.request.sess.post("https://legacy.hackerexperience.com/software",payload)
            if response.status_code != 200:
                Check = Check - 1
            else:
                Check = 0

    def return_to_root(self, sf_id):
        for each in sf_id:
            url = "https://legacy.hackerexperience.com/software.php?action=move&id="+str(each)
            print(url)
            self.request.sess.get(url)

request = request_management
request = (request_management.requestManage())
request.create_new_session()
#request = request.create_new_session()
#print(request)
#print(request.check_if_logged_in())


game = game_info(request)
software, folder = game.grab_local_software_ids_folder_bug()
print(software)
payload = game.move_to_folder(software,folder)
pool = ThreadPool(10)
pool.map(game.send_post_folder, payload)
pool.close()
pool.join()


print("wait")
time.sleep(10)
game.return_to_root(software)
