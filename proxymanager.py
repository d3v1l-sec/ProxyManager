import requests, random, threading, socket, csv, os, sys
from termcolor import colored
from pyfiglet import Figlet

# prints tool banner in slant figlet style
def banner(titel):
    f = Figlet(font='slant')
    print(f.renderText(titel))

def get_user_agent():
    userAgents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)',
        'Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.1.749 Yowser/2.5 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'
    ]
    output = userAgents[random.randint(0, len(userAgents) - 1)]
    return output

class ProxyLoader:
    
    def __init__(self):
        self.proxy_dump = self.export_proxies()

    def create_csv(self, filename, data):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ["protocol", "proxy"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def get_proxies(self):
        os.system("")
        proxy_protocols = ['http', 'https', 'socks4', 'socks5']
        http_proxies = []
        https_proxies = []
        socks4_proxies = []
        socks5_proxies = []
        for protocol in proxy_protocols:
            try:
                response = requests.get(f'https://api.proxyscrape.com/v2/?request=getproxies&protocol={protocol}&timeout=10000&country=all&ssl=all&anonymity=all')
                if response.status_code == 200:
                    proxies = response.text.split('\r\n')
                    if protocol == "http":
                        http_proxies.append(proxies)
                    if protocol == "https":
                        https_proxies.append(proxies)
                    if protocol == "socks4":
                        socks4_proxies.append(proxies)
                    if protocol == "socks5":
                        socks5_proxies.append(proxies)
                else:
                    print(f"[-] Failed to fetch proxies. Status code: {response.status_code}".upper())
            except Exception as e:
                print("[ERROR] Fetching proxies failed:".upper(), e)
        
        print("|"+"_"*44)   
        print("|")     
        print("| ", colored(f"[COLLECTED PROXIES]", 'green', attrs=['reverse', 'blink']), "\t[HTTP]", colored(f"\t\t{str(len(http_proxies[0]))}", "green"))
        print("| ",colored(f"[COLLECTED PROXIES]", 'green', attrs=['reverse', 'blink']), "\t[HTTPS]", colored(f"\t{str(len(https_proxies[0]))}", "green"))
        print("| ",colored(f"[COLLECTED PROXIES]", 'green', attrs=['reverse', 'blink']), "\t[SOCKS4]", colored(f"\t{str(len(socks4_proxies[0]))}", "green"))
        print("| ",colored(f"[COLLECTED PROXIES]", 'green', attrs=['reverse', 'blink']), "\t[SOCKS5]", colored(f"\t{str(len(socks5_proxies[0]))}", "green"))
                
        return http_proxies, https_proxies, socks4_proxies, socks5_proxies
            
    def prepare_csv(self, http_proxies, https_proxies, socks4_proxies, socks5_proxies):
        data_dump = []
        for http_p in http_proxies:
            for proxy in http_p:
                data = {'protocol': 'http', 'proxy': f'{proxy}'}
                data_dump.append(data)
        for https_p in https_proxies:     
            for proxy in https_p:    
                data = {'protocol': 'https', 'proxy': f'{proxy}'}
                data_dump.append(data)
        for sock4_p in socks4_proxies:     
            for proxy in sock4_p:    
                data = {'protocol': 'socks4','proxy': f'{proxy}'}
                data_dump.append(data)
        for socks5_p in socks5_proxies:     
            for proxy in socks5_p:    
                data = {'protocol': 'socks5','proxy': f'{proxy}'}
                data_dump.append(data)
                
        return data_dump

    # Embetted an nice process output while exporting the data
    def export_proxies(self):
        
        print("#"*45)        
        print("| [...] Start scraping proxy ip addresses".upper())
        print("#"*45)
        http_proxies, https_proxies, socks4_proxies, socks5_proxies = self.get_proxies()
        print("|"+"_"*44)
        print("| [...] Prepare data to format as csv.".upper())
        print("|"+"_"*44)
        data_dump = self.prepare_csv(http_proxies, https_proxies, socks4_proxies, socks5_proxies)
        csv_file = "proxies.csv"
        print(f"| [+] Export {str(len(data_dump))} ip addresses to {csv_file}".upper())
        try:
            self.create_csv(csv_file, data_dump)
        except:
            print("[ERROR] File export failed.".upper)
        print("#"*45)   

class ProxyChecker:
    
    def __init__(self, proxy_protocol):
        self.proxy_protocol = proxy_protocol
    
    def import_proxy_data(self):
        csv_file = "proxies.csv"
        proxy_import = []
        with open(csv_file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if any(self.proxy_protocol.lower() in cell.lower() for cell in row):
                    if row[0] == self.proxy_protocol:
                        proxy_import.append(row)
        return proxy_import
    
    def extract_filtered_proxies(self):
        protocol_selection = self.import_proxy_data()
        return protocol_selection
    
    def validate_connection(self, proxy):
        user_agent = get_user_agent()
        headers = {
            'User-Agent': f'{user_agent}',
            'Referer': 'https://www.google.com',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        try:
            check_response = requests.get(url="https://cloudflare.com", headers=headers, proxies={'proxy': f'{proxy}'})
            if check_response.status_code == 200:
                print(colored("[CONNECTION SUCCESSFULL]", "light_green"), proxy, colored("\t[STATUS]", "cyan"), check_response.status_code, colored("\t[RESPONSE BY]"), check_response.url)
        except:
            pass
        
    def export_proxies_to_txt(self):
        proxy_import_data = self.extract_filtered_proxies()
        filename = f"{self.proxy_protocol}-proxies.txt"
        with open(filename, "w") as f:
            for proxy_d in proxy_import_data:
                self.validate_connection(str(proxy_d[1]))
                f.write(str(proxy_d[1])+"\n")
        f.close()


def main():
    
    os.system("")
    banner("ProxyManager")
    
    try:
    
        ProxyLoader()
        
        proxy_protocol = input("\n[?] CHOOSE PROXY PROTOCOL\n\n[+]\tHTTP\n[+]\tHTTPS\n[+]\tSOCKS4\n[+]\tSOCKS5\n\n[SELECT PROXY PROTOCOL]> ").lower()
        print("")
        check = ProxyChecker(proxy_protocol=proxy_protocol)
        check.export_proxies_to_txt()
        
    except KeyboardInterrupt:
        sys.exit()

    
if __name__ == '__main__':
    
    try:
    
        main()
        
    except KeyboardInterrupt:
        sys.exit()