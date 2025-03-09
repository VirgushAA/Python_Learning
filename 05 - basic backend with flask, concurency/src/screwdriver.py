import requests
import argparse
import os

parser = argparse.ArgumentParser(description="Interact with Flask file upload server")
parser.add_argument('--list', action='store_true', help='shows list of files in downloads directory')
parser.add_argument('--upload', help='uploads file to download directory')
args = parser.parse_args()


def list_files():
    """Retrieve the list of files from the screwdriver server."""
    req = requests.get('http://127.0.0.1:8888/files')
    try:
        files = req.json()
        req.raise_for_status()
        print('List of files:')
        for file in files:
            print(file)
    except requests.exceptions.RequestException as e:
        print(f'failed to get file list. Status Code: {e}')


def upload_file(filename):
    """Uploads file to screwdriver server"""
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return

    try:
        with open(filename, 'rb') as f:
            files = {'file': (os.path.basename(filename), f)}
            req = requests.post('http://127.0.0.1:8888/upload', files=files, allow_redirects=False)

        if req.status_code == 302:
            print('File uploaded successfully')
        else:
            print(f'Failed to upload file. Status Code: {req.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error durin file upload: {e}')


def main():
    if args.list:
        list_files()
    elif args.upload:
        upload_file(args.upload)
    else:
        print("You need to specify either --list or --upload <file_path>")
        parser.print_help()


if __name__ == '__main__':
    main()
