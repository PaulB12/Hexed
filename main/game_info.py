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
                proc_desc = list()
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
                    pr_cl = "span4 processBlock"+each
                    proc_desc.append(proc_html.find('div', {'class': pr_cl}).find('div',{'class':'proc-desc'}).text)

                return(proc_id, time_left, proc_completed, proc_desc)
            else:
                return(False)
        else:
            return(False)
    def grab_remote_software(self, ignore_folder):
        url = "https://legacy.hackerexperience.com/internet?view=software"
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):

            soup = BeautifulSoup(web_resp.text, 'html.parser')
            proc = soup.find_all('div', {'class':'span9'})[1]
            regex = r'id\=\"[\d]+\"'
            matches = re.findall(regex, str(proc))
            folder = list()
            software = list()
            software_name = list()
            software_type = list()
            software_version = list()
            software_size = list()
            software_status = list()
            software_virus_own = list()
            software_is_installed_virus = list()
            for procid in matches:
                procid = procid.split('id="')[1].split('"')[0]

                proc2 = (proc.find('tr', {'id':str(procid)}))
                software_status.append(proc2['class'])
                if 'installed' in proc2['class']:
                    try:
                        span_info = (proc2.find_all('span',{'class':'he16-97 tip-top'}))
                        if(len(span_info) >= 1):
                            if "Virus" in str(span_info) and "Doom" not in str(span_info):
                                software_is_installed_virus.append(procid)
                        span_info = (proc2.find_all('span',{'class':'he16-96 tip-top'}))
                        if(len(span_info) >= 1):
                            if "Doom virus" in str(span_info):
                                software_virus_own.append(procid)
                    except:
                        pass

                if 'Folder' in str(proc2):
                    folder.append(procid)
                else:
                    proc_data = proc2.find_all('td')
                    name_type = proc_data[1].text.replace("\n","").split(".")
                    size = proc_data[3].text.replace("\n","")
                    if "MB" in size:
                        size = float(size.replace(" MB",""))
                    elif "GB" in size:
                        size = float(size.replace(" GB","")) * 1000
                    software_size.append(size)
                    software_name.append(name_type[0])
                    software_type.append(name_type[1])
                    software_version.append(proc_data[2].text.replace("\n",""))
                    software.append(procid)
            if len(folder) >= 1 and ignore_folder != 1:
                for each in folder:
                    url = "https://legacy.hackerexperience.com/internet?view=software&cmd=folder&folder="+str(each)
                    web_resp = self.request.get_request(url, 3, 5, 0)
                    if(web_resp != False):
                        soup = BeautifulSoup(web_resp.text, 'html.parser')
                        proc = soup.find_all('div', {'class':'span9'})[1]
                        regex = r'id\=\"[\d]+\"'
                        matches = re.findall(regex, str(proc))
                        for procid in matches:
                            procid = procid.split('id="')[1].split('"')[0]

                            proc2 = (proc.find('tr', {'id':str(procid)}))
                            software_status.append(proc2['class'])
                            if 'installed' in proc2['class']:
                                try:
                                    span_info = (proc2.find_all('span',{'class':'he16-97 tip-top'}))
                                    if(len(span_info) >= 1):
                                        if "Virus" in str(span_info) and "Doom" not in str(span_info):
                                            software_is_installed_virus.append(procid)
                                    span_info = (proc2.find_all('span',{'class':'he16-96 tip-top'}))
                                    if(len(span_info) >= 1):
                                        if "Doom virus" in str(span_info):
                                            software_virus_own.append(procid)
                                except:
                                    pass


                            proc_data = proc2.find_all('td')
                            name_type = proc_data[1].text.replace("\n","").split(".")
                            size = proc_data[3].text.replace("\n","")
                            if "MB" in size:
                                size = float(size.replace(" MB",""))
                            elif "GB" in size:
                                size = float(size.replace(" GB","")) * 1000
                            software_size.append(size)
                            software_name.append(name_type[0])
                            software_type.append(name_type[1])
                            software_version.append(proc_data[2].text.replace("\n",""))
                            software.append(procid)
            return(software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus)
    def grab_local_software(self):
        url = "https://legacy.hackerexperience.com/software"
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):

            soup = BeautifulSoup(web_resp.text, 'html.parser')
            proc = soup.find('div', {'class':'span9'})
            regex = r'id\=\"[\d]+\"'
            matches = re.findall(regex, str(proc))
            folder = list()
            software = list()
            software_name = list()
            software_type = list()
            software_version = list()
            software_size = list()
            software_status = list()
            for procid in matches:
                procid = procid.split('id="')[1].split('"')[0]
                proc2 = (proc.find('tr', {'id':str(procid)}))
                if 'Folder' in str(proc2):
                    folder.append(procid)
                else:
                    proc_data = proc2.find_all('td')
                    name_type = proc_data[1].text.replace("\n","").split(".")
                    #print(procid)
                    software_name.append(name_type[0])
                    software_type.append(name_type[1])
                    software_version.append(proc_data[2].text.replace("\n",""))
                    software.append(procid)
            print(software_type)
            return(False)

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
    def defense_mode(self):
        print("Activiating Defense Mode...")
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
#software, folder = game.grab_local_software_ids_folder_bug()
#print(software)
#payload = game.move_to_folder(software,folder)
#pool = ThreadPool(10)
#pool.map(game.send_post_folder, payload)
#pool.close()
#pool.join()


#print("wait")
#time.sleep(10)
#game.return_to_root(software)
print(game.grab_remote_software())
