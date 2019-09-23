import requests

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; America Online Browser 1.1; Windows NT 5.1; FunWebProducts)'

github_api_url = 'https://api.github.com/users/'

user_name='Belfi-Gor'

response = requests.get(f'{github_api_url}{user_name}/repos', headers={'User-Agent': USER_AGENT})

data = response.json()

rep_list = {}

print(data)

for row in data:
    print(f'{row["name"]} - {row["description"]}')