import requests
import os

def download_and_replace_file(url, directory, filename):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Full path to save the file
    file_path = os.path.join(directory, filename)

    # Download the file
    print(f"Downloading {filename} from {url}")
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Write the content to the file, replacing it if it already exists
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Successfully downloaded and saved {filename} to {directory}")
    else:
        print(f"Failed to download file: HTTP {response.status_code}")

# Example usage
if __name__ == "__main__":
    url = "https://cdn-sp.totogaming.am/assets/fonts/sport-icons/sportsIcons.ttf?123"
    directory = "src"
    filename = "source_empty_font.ttf"
    download_and_replace_file(url, directory, filename)



    