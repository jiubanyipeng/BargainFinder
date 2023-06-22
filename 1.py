import requests

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
s = 'https://search.jd.com/Search?keyword=GeForce%20RTX%204060&pvid=311f899c1d9c495cbbc63dcf90922bcf&page=17&s=481&click=0'


print(requests.get(s,headers=headers).status_code)






