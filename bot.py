import requests
import json
import os
import urllib.parse
import hashlib
from core.helper import get_headers, countdown_timer, extract_user_data, config
from colorama import *
from os import system as sys
from base64 import urlsafe_b64decode
import random
from platform import system as s_name
from datetime import datetime
import time


class FreeDOGS:
    def __init__(self) -> None:
        self.session = requests.Session()


    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        banner = f"""{Fore.GREEN}
                                         ██████  ██    ██   ██████  ██    ██  ███    ███  ██████   ███████  ██████  
                                        ██       ██    ██  ██       ██    ██  ████  ████  ██   ██  ██       ██   ██ 
                                        ██       ██    ██  ██       ██    ██  ██ ████ ██  ██████   █████    ██████  
                                        ██       ██    ██  ██       ██    ██  ██  ██  ██  ██   ██  ██       ██   ██ 
                                         ██████   ██████    ██████   ██████   ██      ██  ██████   ███████  ██   ██     
                                            """
        print(Fore.GREEN + Style.BRIGHT + banner + Style.RESET_ALL)
        print(Fore.GREEN + f" Free Dogs Bot")
        print(Fore.RED + f" FREE TO USE = Join us on {Fore.GREEN}t.me/cucumber_scripts")
        print(Fore.YELLOW + f" before start please '{Fore.GREEN}git pull{Fore.YELLOW}' to update bot")
        print(f"{Fore.WHITE}~" * 60)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def extract_user_data(self, query: str) -> str:
        user_data_encoded = query.split('user%3D')[1].split('%26')[0]

        if user_data_encoded:
            user_data = urllib.parse.unquote(urllib.parse.unquote(user_data_encoded))
            user_json = json.loads(user_data)
            return str(user_json.get('first_name', 'Unknown'))
        return 'Unknown'


    def load_tokens(self):
        try:
            if not os.path.exists('tokens.json'):
                return {"accounts": []}

            with open('tokens.json', 'r') as file:
                data = json.load(file)
                if "accounts" not in data:
                    return {"accounts": []}
                return data
        except json.JSONDecodeError:
            return {"accounts": []}

    def save_tokens(self, tokens):
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file, indent=4)

    def generate_tokens(self, queries: list):
        tokens_data = self.load_tokens()
        accounts = tokens_data["accounts"]

        for idx, query in enumerate(queries):
            account_name = self.extract_user_data(query)

            existing_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)

            if not existing_account:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Token Is None{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Generating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)

                token = self.get_token(query)
                if token:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )
                    accounts.insert(idx, {"first_name": account_name, "token": token})
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)

        self.save_tokens({"accounts": accounts})

    def renew_token(self, account_name):
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])
        
        account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        
        if account and "token" in account:
            token = account["token"]
            if not self.mine_info(token):
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Token Isn't Valid{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Regenerating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)
                
                accounts = [acc for acc in accounts if acc["first_name"] != account_name]
                
                query = next((query for query in self.load_queries() if self.extract_user_data(query) == account_name), None)
                if query:
                    new_token = self.get_token(query)
                    if new_token:
                        accounts.append({"first_name": account_name, "token": new_token})
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Query Is None. Skipping {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
        
        self.save_tokens({"accounts": accounts})

    def load_queries(self):
        with open('query.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
        
    def user_auth(self, query: str):
        url = f"https://api.freedogs.bot/miniapps/api/user/telegram_auth?invitationCode=MExkDhtZ&initData={query}"
        body = {'initData':query}
        self.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.post(url, headers=self.headers, data=body)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']['token']
        else:
            return None
        
    def mine_info(self, token: str):
        url = 'https://api.freedogs.bot/miniapps/api/mine/getMineInfo?'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.get(url, headers=self.headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return False
        
    def game_info(self, token: str):
        url = 'https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo?'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.get(url, headers=self.headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
    
    def generate_hash(self, amount: str, seq_no: str):
        static_string = "7be2a16a82054ee58398c5edb7ac4a5a"
        combined = str(amount) + str(seq_no) + static_string
        return hashlib.md5(combined.encode()).hexdigest()

    def collect_coin(self, token: str, amount: str, hash_code: str, seq_no: str):
        url = "https://api.freedogs.bot/miniapps/api/user_game/collectCoin?"
        data = {'collectAmount': amount, 'hashCode': hash_code, 'collectSeqNo': seq_no}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.post(url, headers=self.headers, data=data, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
        
    def tasks_list(self, token: str):
        url = 'https://api.freedogs.bot/miniapps/api/task/lists?'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.get(url, headers=self.headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']['lists']
        else:
            return None
        
    def finish_tasks(self, token: str, task_id: str):
        url = f'https://api.freedogs.bot/miniapps/api/task/finish_task?id={task_id}'
        data = json.dumps({'id': task_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result
        else:
            return None
    def set_proxy(self, proxy):
        self.session.proxies = {
            "http": proxy,
            "https": proxy,
        }
        if '@' in proxy:
            host_port = proxy.split('@')[-1]
        else:
            host_port = proxy.split('//')[-1]
        return host_port

    def save_token(self, id, token):
        tokens = json.loads(open("tokens.json").read())
        tokens[str(id)] = token
        open("tokens.json", "w").write(json.dumps(tokens, indent=4))

    def get_token(self, id):
        tokens = json.loads(open("tokens.json").read())
        if str(id) not in tokens.keys():
            return None
        return tokens[str(id)]

    def is_expired(self, token):
        header, payload, sign = token.split(".")
        deload = urlsafe_b64decode(payload + "==").decode()
        jeload = json.loads(deload)
        now = int(datetime.now().timestamp())
        if now > jeload["exp"]:
            return True
        return False

    def process_query(self, query: str, id:str, user_name:str):

        token = self.get_token(id)
        if token is None:
            token = self.user_auth(query)
            if token is None:
                return
            self.save_token(id, token)

        if self.is_expired(token):
            token = self.user_auth(query)
            if token is None:
                return
            self.save_token(id, token)

        if token:

            mine_info = self.mine_info(token)

            if mine_info:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user_name} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {mine_info['getCoin']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

                game = self.game_info(token)
                if game:
                    max_click = game['userToDayMaxClick']
                    today_click = game['userToDayNowClick']
                    amount = int(game['coinPoolLeft'])
                    seq_no = int(game['collectSeqNo'])
                    hash_code = self.generate_hash(amount, seq_no)

                    if today_click < max_click:
                        collect = self.collect_coin(token, amount, hash_code, seq_no)
                        if collect:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {collect['collectAmount']} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} is Failed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(f"{Fore.YELLOW + Style.BRIGHT}[ Tap Tap Reached Maximum Limit ]{Style.RESET_ALL}")
                else:
                    self.log(f"{Fore.RED+Style.BRIGHT}[ Error Fetching Game Info ]{Style.RESET_ALL}")

                tasks = self.tasks_list(token)
                completed_tasks = False
                if tasks:
                    for task in tasks:

                        if task['isFinish'] == 0:
                            task_id = task['id']

                            finish = self.finish_tasks(token, task_id)
                            if finish:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} is Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['rewardParty']} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} is Failed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                        else:
                            completed_tasks = True

                    if completed_tasks:
                        self.log(f"{Fore.YELLOW+Style.BRIGHT}[ All Available Task is Completed ]{Style.RESET_ALL}")
                else:
                    self.log(f"{Fore.RED+Style.BRIGHT}[ Error Fetching Tasks Info ]{Style.RESET_ALL}")
        
    def main(self):
        try:

            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]
            with open('proxies.txt', 'r') as file:
                proxies = [line.strip() for line in file if line.strip()]


            while True:
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Proxy's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(proxies)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for i, query in enumerate(queries):
                    query = query.strip()
                    if query:
                        self.log(
                            f"{Fore.GREEN + Style.BRIGHT}Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{i + 1} / {len(queries)}{Style.RESET_ALL}"
                        )
                        if len(proxies) >= len(queries):
                            proxy = self.set_proxy(proxies[i])  # Set proxy for each account
                            self.log(
                                f"{Fore.GREEN + Style.BRIGHT}Use proxy: {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
                            )

                        else:
                            self.log(
                                Fore.RED + "Number of proxies is less than the number of accounts. Proxies are not used!")

                        user_info = extract_user_data(query)
                        user_id = str(user_info.get('id'))
                        user_name = str(user_info.get('username'))
                        self.headers = get_headers(user_id)

                        try:
                            self.process_query(query, user_id, user_name)
                        except Exception as e:
                            self.log(f"{Fore.RED + Style.BRIGHT}An error process_query: {e}{Style.RESET_ALL}")

                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)
                        account_delay = config['account_delay']
                        countdown_timer(random.randint(min(account_delay), max(account_delay)))

                cycle_delay = config['cycle_delay']
                countdown_timer(random.randint(min(cycle_delay), max(cycle_delay)))

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Free DOGS - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    if s_name() == 'Windows':
        sys(f'Free Dogs')
    else:
        sys('clear')
    freedogs = FreeDOGS()
    freedogs.clear_terminal()
    freedogs.welcome()
    freedogs.main()
