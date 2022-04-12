import json
import re
import time
import requests
from Wappalyzer import Wappalyzer, WebPage
from dotenv import load_dotenv
import os

load_dotenv()
validIpAddressRegex = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
validURLRegex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

name_file_ip_candidates = 'data/ip_candidates.txt'
name_file_url_candidates = 'data/url_candidates.txt'
name_file_mac_candidates = 'data/mac_candidates.txt'
name_file_result_cms = 'result_cms.txt'
name_file_result = 'final_result.txt'
auth = os.getenv('AUTH')


def separated_files():
    """ doc """
    # ---------------------data mac address-----------------
    raw_data_mac_address = open('../mac-vendor.txt', 'rb').readlines()
    file_mac = open(name_file_mac_candidates, 'w', encoding='utf8')
    data_mac = {}
    for mac in raw_data_mac_address:
        information_mac = mac.decode('utf-8').strip().split('\t')
        data_mac[information_mac[0]] = information_mac[1]
    json_data_mac = json.dumps(data_mac)
    file_mac.write(json_data_mac)
    file_mac.close()
    # ----------------------data IP address--------------------
    raw_data = open('../flag.txt').read()
    ip_candidates = re.findall(validIpAddressRegex, raw_data)
    file_ip = open(name_file_ip_candidates, 'w', encoding='utf8')
    for ip in ip_candidates:
        file_ip.write(ip)
        file_ip.write("\n")
    file_ip.close()
    # ----------------------data URL--------------------
    url_candidates = re.findall(validURLRegex, raw_data)
    file_url = open(name_file_url_candidates, 'w', encoding='utf8')
    for url in url_candidates:
        file_url.write(url)
        file_url.write("\n")
    file_url.close()
    print('done Separated file!')


def get_cms_use_url():
    print('start get CMS use url')
    drupal = 0
    joomla = 0
    wordPress = 0
    others = 0
    file_cms = open(name_file_result_cms, 'w', encoding='utf8')
    information = []
    data_url = open('data/url_candidates.txt').read()
    data_url_list = data_url.split('\n')
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

    for url in data_url_list:
        if url:
            response = requests.get(url, headers=header)
            wappalyzer = Wappalyzer.latest()
            webpage = WebPage.new_from_response(response)
            result = wappalyzer.analyze_with_categories(webpage)
            if result.get('Drupal') is not None:
                information_result = {}
                information_result.update({'URl': url, 'CMS': 'Drupal'})
                information.append(information_result)
                drupal += 1
            elif result.get('Joomla') is not None:
                information_result = {}
                information_result.update({'URl': url, 'CMS': 'Joomla'})
                information.append(information_result)
                joomla += 1
            elif result.get('WordPress') is not None:
                information_result = {}
                information_result.update({'URl': url, 'CMS': 'WordPress'})
                information.append(information_result)
                wordPress += 1
            else:
                information_result = {}
                information_result.update({'URl': url, 'CMS': 'Not Found', 'Building use': list(result.keys())})
                information.append(information_result)
                others += 1
    print('-----------------get the CMS for every URL ----------------------------')
    result_file.write('-----------------get the CMS for every URL ----------------------------')
    print('(WordPress):', wordPress, '(Joomla):', joomla, '(Drupal):', drupal)
    result_file.write(f'(WordPress):{wordPress}(Joomla):{joomla}(Drupal): {drupal}')
    result_file.write('\n')
    print('---------------------------------------------------------------------')
    result_file.write('---------------------------------------------------------------------')
    file_cms.write(str(information))
    file_cms.close()


def get_ip_use_api():
    print('start get country use data ip')
    russia = 0
    qatar = 0
    spain = 0
    others = 0
    data_ip = open('data/ip_candidates.txt').read()
    data_ip_list = data_ip.split('\n')
    list_information_ip = []
    for ip_address in data_ip_list:
        if ip_address:
            url = f'https://ipgeolocation.abstractapi.com/v1/?api_key={auth}&ip_address=' + ip_address
            response = requests.get(url)
            time.sleep(1)
            data = json.loads(response.text)
            information_ip = {data.get('country'): ip_address}
            list_information_ip.append(information_ip)

    for i in list_information_ip:
        if list(i.keys())[0] == 'Qatar':
            qatar += 1
        elif list(i.keys())[0] == 'Russia':
            russia += 1
        elif list(i.keys())[0] == 'Spain':
            spain += 1
        else:
            others += 1
    print('-----------------Get IP addresses, you have to get the country for every Ip----------------------------')
    print('Total: (Russia):', russia, '(Spain):', spain, '(Qatar):', qatar, '(Others):', others)
    result_file.write(f'Total: (Russia):{russia}(Spain):{spain}(Qatar):{qatar}(Others):{others}')
    result_file.write('\n')
    result_file.write('------------------------------------------------------------------------------------------')
    print(list_information_ip)
    result_file.write(str(list_information_ip))
    print('------------------------------------------------------------------------------------------')


def get_mac_vendor():
    print('start count the number mac address vendor from Apple,Cisco,Samsung.....')
    apple = 0
    cisco = 0
    samsung = 0
    others = 0
    data_mac = open('data/mac_candidates.txt').read()
    data_json = json.loads(data_mac)
    list_data = list(data_json.values())

    for i in list_data:
        if 'Apple' in i:
            apple += 1
        elif 'Cisco' in i:
            cisco += 1
        elif 'Samsung' in i:
            samsung += 1
        else:
            others += 1
    print('-----------------Get MAC addresses, get a mac-vendor for every MAC address----------------------------')
    result_file.write('-----------------Get MAC addresses, get a mac-vendor for every MAC address----------------------------')
    print('Total: (Apple):', apple, '(Cisco):', cisco, '(Samsung):', samsung, '(Others):', others)
    result_file.write(f'Total: (Apple):{apple}(Cisco):{cisco}(Samsung):{samsung}(Others): {others}')
    result_file.write('\n')
    result_file.write('------------------------------------------------------------------------------------------')
    # print(list_data)
    print('------------------------------------------------------------------------------------------')


if __name__ == '__main__':
    result_file = open(name_file_result, 'w', encoding='utf8')
    separated_files()
    get_cms_use_url()
    get_ip_use_api()
    get_mac_vendor()
    result_file.close()
    print('The End !')
