import requests

localhost = '192.168.247.138:8080'

def load_list_filename(api_key):
    url = f'http://{localhost}/list-audio-files'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json().get('files', [])
        if files:
            print("Available files:", files)
        else:
            print("No files available.")
    else:
        print("Failed to retrieve file list:", response.text)


def download_audio(api_key, filename='file1.wav'):
    download_url = f'http://{localhost}/download-audio/{filename}'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(download_url, headers=headers)

    if response.status_code == 200:
        with open(f'./{filename}', 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully")
    else:
        print(f"Failed to download file {filename}: {response.text}")


def load_allFile(api_key):
    url = f'http://{localhost}/download-all-audio'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with open('all_audio_files.zip', 'wb') as f:
            f.write(response.content)
        print("All files downloaded successfully")
    else:
        print("Failed to download all files:", response.text)