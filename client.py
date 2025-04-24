import requests

def main():
    resp = requests.post(
        'http://127.0.0.1:8000/assist/stream',
        files={'audio': open('voice.wav','rb')},
        stream=True
    )
    with open('out.mp3','wb') as f:
        for chunk in resp.iter_content(1024): f.write(chunk)

    print(requests.get(
        'http://127.0.0.1:8000/query/',
        params={'sql':'SELECT * FROM info LIMIT 5'}
    ).json())

    print(requests.get(
        'http://127.0.0.1:8000/db/brands',
        params={'limit':5}
    ).json())

if __name__ == '__main__':
    main()
