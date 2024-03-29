from multiprocessing.dummy import Pool as ThreadPool
import request_management
import re
import time
from datetime import datetime
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
        log_r = self.request.post_request(url,payload,5,10)
        if(log_r != False):
            time.sleep(3.5)
            self.request.get_request(log_r.url, 3, 5, 0)
            return(True)
        else:
            return(False)

    def fetch_active_process(self, type):
        if type == 1:
            url = "https://legacy.hackerexperience.com/processes?page=cpu"
        else:
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
                proc_html = BeautifulSoup(web_resp.text, 'html.parser')
                for each in proc_id:
                    pr_cl = "span4 processBlock"+str(each)
                    print(pr_cl)
                    proc_desc.append(proc_html.find('div', {'class': pr_cl}).find('div',{'class':'proc-desc'}).text)

                return(proc_id, time_left, proc_completed, proc_desc)
            else:
                return(False)
        else:
            return(False)
    def fetch_active_process_network(self):
        url = "https://legacy.hackerexperience.com/processes?page=network"
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
                proc_html = BeautifulSoup(web_resp.text, 'html.parser')
                for each in proc_id:
                    try:
                        pr_cl = "span4 processBlock"+str(each)
                        print(pr_cl)
                        proc_desc.append(proc_html.find('div', {'class': pr_cl}).find('div',{'class':'proc-desc'}).text)
                    except:
                        pass

                return(proc_id, time_left, proc_completed, proc_desc)
            else:
                return(False)
        else:
            return(False)
    def grab_software(self, ignore_folder, type):
        if type == 0:
            url = "https://legacy.hackerexperience.com/internet?view=software"
        else:
            url = "https://legacy.hackerexperience.com/software"
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):

            soup = BeautifulSoup(web_resp.text, 'html.parser')
            if type == 0:
                proc = soup.find_all('div', {'class':'span9'})[1]
            else:
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
                    if type == 0:
                        url = "https://legacy.hackerexperience.com/internet?view=software&cmd=folder&folder="+str(each)
                    else:
                        url = "https://legacy.hackerexperience.com/software?action=folder&view="+str(each)
                    web_resp = self.request.get_request(url, 3, 5, 0)
                    if(web_resp != False):
                        soup = BeautifulSoup(web_resp.text, 'html.parser')
                        if type == 0:
                            proc = soup.find_all('div', {'class':'span9'})[1]
                        else:
                            proc = soup.find('div', {'class':'span9'})
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
            return(software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder)

    def move_to_folder(self,software,folder_id, type):
        if type == 0:
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
        else:
            url = "https://legacy.hackerexperience.com/internet"
            threads = list()
            ac_py = list()
            for soft_id in software:
                payload = {
                    'view':'software',
                    'cmd':'folder',
                    'folder':folder_id,
                    'id':soft_id,
                    'act':'move-folder',
                }
                ac_py.append(payload)
        return(ac_py)
    def defense_mode(self):
        print("Activiating Defense Mode...")
    def send_post_folder(self,payload):
        type = 1
        if type == 0:
            url = "https://legacy.hackerexperience.com/software"
        else:
            url = "https://legacy.hackerexperience.com/internet"
        Check = 3
        while Check > 0:
            response = self.request.sess.post(url,payload)
            if response.status_code != 200:
                Check = Check - 1
            else:
                Check = 0

    def return_to_root(self, sf_id, type):
        for each in sf_id:
            if type == 0:
                url = "https://legacy.hackerexperience.com/software.php?action=move&id="
            else:
                url = "https://legacy.hackerexperience.com/internet?view=software&cmd=move&id="
            url = url+str(each)
            print(url)
            self.request.sess.get(url)
    def delete_folder(self, folder_id, type):
        if type == 0:
            url = "https://legacy.hackerexperience.com/software"
        else:
            url = "https://legacy.hackerexperience.com/internet"

        payload = {
            'act':'delete-folder',
            'id':str(folder_id)
        }
        self.request.sess.post(url,payload)
    def create_folder(self, name, type):
        if type == 0:
            url = "https://legacy.hackerexperience.com/software"
        else:
            url = "https://legacy.hackerexperience.com/internet"
        payload = {
            "name":str(name),
            "act":"create-folder",
            "id":0,
            }
        self.request.sess.post(url,payload)
    def crack_ip(self, ip):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Cracking "+ip+" @ "+current_time)
        url = "https://legacy.hackerexperience.com/internet?action=hack&method=bf&ip="+ip
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if "newbie protection" in web_resp.text:
                print("Failed cracking "+ip+" | Newbie Protection @ "+current_time)
                return(False)
            elif "Access denied" in web_resp.text:
                print("Failed cracking "+ip+" | Access Denied - Trying exploits @ "+current_time)
                url = "https://legacy.hackerexperience.com/internet?action=hack&method=xp&ip="+ip
                return(False)
                exp_resp = self.request.get_request(url, 3, 5, 0)
                if(exp_resp != False):
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    if "Error!" in exp_resp.text:
                        print("Failed exploiting "+ip+" | Software/Failure - All routes tried @ "+current_time)
                        return(False)
                    elif "Port scan" in exp_resp.text:
                        print("Exploiting "+ip+" | Port scan queued @ "+current_time)
                        return(False)
                else:
                    return(False)
            elif "Crack server" in web_resp.text:
                print("Cracking "+ip+" @ "+current_time)
                return(True)
            elif "hacked database" in web_resp.text:
                print("Failed cracking "+ip+" | IP Already hacked @ "+current_time)
                return(True)
            elif "ip does not exist" in web_resp.text:
                print("Failed cracking "+ip+" | IP doesn't exist @ "+current_time)
                return(False)
        else:
            return(False)
    def remote_hardware(self):
        url = "https://legacy.hackerexperience.com/internet?view=software"
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):
            if "HDD Usage" in web_resp.text:
                soup = BeautifulSoup(web_resp.text, 'html.parser')
                data = soup.find_all('span',{'class':'small'})
                internet = data[1].find('strong').text.split(" ")
                if internet[1].lower() == "gbit":
                    internet = float(internet[0]) * 1000
                else:
                    internet = float(internet[0])
                hardware_data = data[2].find_all('font')
                space_used = hardware_data[0].text.split(" ")
                max_space = hardware_data[1].text.split(" ")
                if space_used[1].lower() == "mb":
                    space_used = float(space_used[0])
                else:
                    space_used = float(space_used[0]) * 1000
                if max_space[1].lower() == "mb":
                    max_space = float(max_space[0])
                else:
                    max_space = float(max_space[0]) * 1000
                return (internet, space_used, max_space)

            else:
                return(False, False, False)
        else:
            return(False, False, False)
    def login_to_ip(self, ip):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("Attempting to log into "+ip+" @ "+current_time)
        url = "https://legacy.hackerexperience.com/internet?ip="+ip+"&action=hack&method=bf"
        web_resp = self.request.get_request(url, 3, 5, 0)
        if(web_resp != False):
            if "hacked database" in web_resp.text:
                url = "https://legacy.hackerexperience.com/internet?action=login"
                url_resp = self.request.get_request(url, 3, 5, 0)
                if(url_resp != False):
                    soup = BeautifulSoup(url_resp.text, 'html.parser')
                    password = soup.find('input', {'name': 'pass'}).get('value')
                    pass_url = 'https://legacy.hackerexperience.com/internet?action=login&user=root&pass='+password
                    pass_resp = self.request.get_request(pass_url, 3, 5, 0)
                    if(url_resp != False):
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("Logged into "+ip+" @ "+current_time)
                        return(True)
                    else:
                        return(False)
                else:
                    return(False)
            else:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("Failed logging | IP "+ip+" | Not in Hacked Database @ "+current_time)
        else:
            return(False)
    def find_best_virus(self, space, type):
        ddos_id = list()
        ddos_name = list()
        ddos_version = list()
        ddos_space = list()
        vminer_id = list()
        vminer_name = list()
        vminer_version = list()
        vminer_space = list()
        software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = self.grab_software(0, 1)
        counter = 0
        for each in software_type:
            if each == "vddos":
                if software_size[counter] <= space:
                    ddos_id.append(software[counter])
                    ddos_name.append(software_name[counter])
                    ddos_version.append(software_version[counter])
                    ddos_space.append(software_size[counter])
            if each == "vminer":
                if software_size[counter] <= space:
                    vminer_id.append(software[counter])
                    vminer_name.append(software_name[counter])
                    vminer_version.append(software_version[counter])
                    vminer_space.append(software_size[counter])
            counter = counter + 1
        if type == "vddos":
            final_counter = 0
            counter = 0
            max = 0
            if len(ddos_version) == 0:
                return(False, False, False, False)
            for each in ddos_version:
                if float(each) > float(max):
                    max=each
                    final_counter = counter
                counter = counter + 1
            return(ddos_id[final_counter], ddos_name[final_counter], ddos_version[final_counter], ddos_space[final_counter])

        elif type == "vminer":
            final_counter = 0
            counter = 0
            max = 0
            if len(vminer_version) == 0:
                return(False, False, False, False)
            for each in vminer_version:
                if float(each) > float(max):
                    max=each
                    final_counter = counter
                counter = counter + 1
            return(vminer_id[final_counter], vminer_name[final_counter], vminer_version[final_counter], vminer_space[final_counter])
    def upload_software(self, soft_id):
        url = 'https://legacy.hackerexperience.com/internet?view=software&cmd=up&id='+str(soft_id)
        resp = self.request.get_request(url, 3, 5, 0)
        if resp != False:
            return(True)
        else:
            return(False)
    def internet_logout(self):
        self.request.get_request("https://legacy.hackerexperience.com/internet?view=logout", 3, 5, 0)
        return(True)
    def fetch_active_uploads(self):
        proc_id, time_left, proc_completed, proc_desc = (self.fetch_active_process())
        proc_counter = 0
        virus_uploaded_id = list()
        virus_uploaded_name = list()
        virus_uploaded_version = list()
        virus_uploaded_ip = list()
        virus_uploaded_completed = list()
        virus_uploaded_timeleft = list()
        for each in proc_desc:
            if "Upload file" in each:
                each = each.replace("Upload file ","")
                name_data = each.split(" at ")
                name_version = name_data[0].split("(")
                name = name_version[0]
                version = name_version[1].split(")")[0]
                ip = name_data[1]
                virus_uploaded_id.append(proc_id[proc_counter])
                virus_uploaded_name.append(name)
                virus_uploaded_version.append(version)
                virus_uploaded_ip.append(ip)
                virus_uploaded_completed.append(proc_completed[proc_counter])
                virus_uploaded_timeleft.append(time_left[proc_counter])
            proc_counter = proc_counter + 1
        return(virus_uploaded_id, virus_uploaded_name, virus_uploaded_version, virus_uploaded_ip, virus_uploaded_completed, virus_uploaded_timeleft)
    def virus_upload_complete(self):
        proc_id, time_left, proc_completed, proc_desc = (self.fetch_active_process_network())
        proc_counter = 0
        virus_uploaded_id = list()
        virus_uploaded_name = list()
        virus_uploaded_version = list()
        virus_uploaded_ip = list()
        virus_uploaded_completed = list()
        virus_uploaded_timeleft = list()
        for each in proc_desc:
            if "Upload file" in each:
                each = each.replace("Upload file ","")
                name_data = each.split(" at ")
                name_version = name_data[0].split("(")
                name = name_version[0]
                version = name_version[1].split(")")[0]
                ip = name_data[1]
                virus_uploaded_id.append(proc_id[proc_counter])
                virus_uploaded_name.append(name)
                virus_uploaded_version.append(version)
                virus_uploaded_ip.append(ip)
                virus_uploaded_completed.append(proc_completed[proc_counter])
                virus_uploaded_timeleft.append(time_left[proc_counter])
            proc_counter = proc_counter + 1
        soft_counter = 0
        virus_uploaded_id = virus_uploaded_id[::-1]
        virus_uploaded_name = virus_uploaded_name[::-1]
        virus_uploaded_version = virus_uploaded_version[::-1]
        virus_uploaded_ip = virus_uploaded_ip[::-1]
        virus_uploaded_completed = virus_uploaded_completed[::-1]
        virus_uploaded_timeleft = virus_uploaded_timeleft[::-1]
        for ip in virus_uploaded_ip:
            if virus_uploaded_timeleft[soft_counter] != 0:
                time.sleep(int(virus_uploaded_timeleft[soft_counter]))
            game.login_to_ip(ip)
            game.internet_logs()
            url = "https://legacy.hackerexperience.com/processes?pid="+virus_uploaded_id[soft_counter]
            resp = self.request.get_request(url, 3, 5, 0)
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("Virus Uploaded @ "+current_time)
            if resp != False:
                software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = self.grab_software(1, 0)
                sep_counter = 0
                for each in software_name:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print("Finding uploaded virus @ "+current_time)
                    if each in virus_uploaded_name[soft_counter]:
                        url2 = "https://legacy.hackerexperience.com/internet?view=software&cmd=install&id="+str(software[sep_counter])
                        self.request.get_request(url2, 3, 5, 0)
                        time.sleep(4)
                        self.request.get_request(url2, 3, 5, 0)
                        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("Virus installed | Logging out @ "+current_time)
                    sep_counter = sep_counter + 1
            soft_counter = soft_counter + 1
            self.internet_logout()
    def internet_logs(self):
        try:
            url = "https://legacy.hackerexperience.com/internet?view=logs"
            log_resp = self.request.get_request(url, 3, 5, 0)
            if log_resp != False:
                soup = BeautifulSoup(log_resp.text, 'html.parser')
                log = soup.find('textarea', {'class':'logarea'})
                ips = self.parse_log(log.text)
                with open("new_ips.txt","a") as ip_log:
                    for ip in ips:
                        ip = ip + "\n"
                        ip_log.writelines(ip)
                return(ips)
            else:
                return(False)
        except:
            return(False)
    def change_password(self):
        url = "https://legacy.hackerexperience.com/index"
        payload = {
            'acc':'192124626',
            'act':'changepwd',
        }
        self.request.post_request(url, payload, 3, 2)
        proc_id, time_left, proc_completed, proc_desc = self.fetch_active_process(1)
        counter = 0
        reset_id, reset_time = self.check_password_status()
        if reset_time == 0:
            with open("password_id.txt","w") as file:
                file.writelines(str(reset_password))
    def check_password_status(self):
        proc_id, time_left, proc_completed, proc_desc = self.fetch_active_process(1)
        counter = 0
        for each in proc_desc:
            if "Reset password file" in each:
                reset_password = proc_id[counter]
                reset_time = time_left[counter]
                print("RESET TIME")
                print(reset_time)
            counter = counter + 1
        if reset_time == 0:
            return(reset_password, reset_time)
        else:
            return(False, reset_time)
    def complete_password(self):
        with open("password_id.txt","r") as file:
            proc_id = file.readlines()[0]
        url = "https://legacy.hackerexperience.com/processes?pid="+proc_id
        resp = self.request.get_request(url, 3, 5, 0)
    def defense_hide_software(self, time_s):
        self.create_folder('start', 1)
        software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = self.grab_software(1, 1)
        import_software = list()
        counter = 0
        for each in software_type:
            if 'fwl' in each or 'hash' in each or 'vddos' in each or 'crc' in each:
                import_software.append(software[counter])
            counter = counter + 1
        print(folder[0])
        t_end = time.time() + time_s
        while time.time() < t_end:
            software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = self.grab_software(1, 1)
            payload = self.move_to_folder(import_software,folder[-1],0)
            pool = ThreadPool(5)
            pool.map(self.send_post_folder, payload)
            pool.close()
            pool.join()
            time.sleep(1.5)
            self.create_folder(folder[-1], 0)
            self.return_to_root(import_software, 0)
            self.delete_folder(folder[-1], 0)
        try:
            self.return_to_root(import_software, 0)
            software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = self.grab_software(1, 1)
            for folder_id in folder:
                self.delete_folder[folder_id, 0]
        except:
            pass
    def check_for_intruder(self):
        log = self.grab_local_log()
        regex = r"[[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+] logged in"
        matches = re.findall(regex, log)
        if(len(matches) >= 1):
            return(True)
        else:
            return(False)


request = request_management
request = (request_management.requestManage())
request.create_new_session()
#request = request.create_new_session()
#print(request)
#print(request.check_if_logged_in())


game = game_info(request)
def be_annoying_prick():
    game.create_folder('start', 1)
    software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = game.grab_software(1, 1)
    import_software = list()
    counter = 0
    for each in software_type:
        if 'fwl' in each:
            import_software.append(software[counter])
        counter = counter + 1
    while True:
        software, software_name, software_type, software_version, software_size, software_status, software_virus_own, software_is_installed_virus, folder = game.grab_software(1, 1)
        print(folder[-1])
        payload = game.move_to_folder(import_software,folder[-1],1)
        pool = ThreadPool(5)
        pool.map(game.send_post_folder, payload)
        pool.close()
        pool.join()
        time.sleep(1)
        game.create_folder(folder[-1], 1)
        game.return_to_root(import_software, 1)
        game.delete_folder(folder[-1], 1)
#game.change_password()
#game.wipe_local_log
game.change_password()
while True:
    time.sleep(1.5)
    intruder = game.check_for_intruder()
    while intruder:
        print("Intruder Detected | Activating Defense")
        pass_id, pass_time = game.check_password_status()
        print(pass_id)
        print(pass_time)
        intruder = False
        if int(pass_time) == 0:
            game.complete_password()
            game.wipe_local_log()
            print("Intruder Kicked out of system!")
            game.change_password()
            intruder = False
        else:
            game.defense_hide_software(int(pass_time))
            print("Intruder Detected | Software Hiding Enabled")
