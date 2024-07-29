import requests
import hashlib
import subprocess
import os

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256(version= '3.0.21'):
    """Downloads the text file containing the expected SHA-256 value for the VLC installer file from the 
    videolan.org website and extracts the expected SHA-256 value from it.

    Returns:
        str: Expected SHA-256 hash value of VLC installer
    """
    # TODO: Step 1
    # Hint: See example code in lab instructions entitled "Extracting Text from a Response Message Body"
    file_url = f'https://download.videolan.org/pub/videolan/vlc/{version}/win64/vlc-{version}-win64.exe.sha256'
    resp_msg = requests.get(file_url)

    #check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
    
        print(f'Success!')
        #extract test file content from response message body
        file_content = resp_msg.text
        #
        expected_sha256 = file_content[:64]
    
        print('expected_sha256 of vlc installer:', expected_sha256)
        
        return expected_sha256
    else:
        print (f'Failure!')
        pass
    
    

def download_installer(version = '3.0.21'):
    """Downloads, but does not save, the .exe VLC installer file for 64-bit Windows.

    Returns:
        bytes: VLC installer file binary data
    """
    
    # Hint: See example code in lab instructions entitled "Downloading a Binary File"
    file_url = f'https://download.videolan.org/pub/videolan/vlc/{version}/win64/vlc-{version}-win64.exe'
    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:
        file_content =resp_msg.content
    
        
    return file_content

def installer_ok(installer_data, expected_sha256):
    """Verifies the integrity of the downloaded VLC installer file by calculating its SHA-256 hash value 
    and comparing it against the expected SHA-256 hash value. 

    Args:
        installer_data (bytes): VLC installer file binary data
        expected_sha256 (str): Expeced SHA-256 of the VLC installer

    Returns:
        bool: True if SHA-256 of VLC installer matches expected SHA-256. False if not.
    """    
    # Step 3
    # Hint: See example code in lab instructions entitled "Computing the Hash Value of a Response Message Body"

    image_hash =hashlib.sha256(installer_data).hexdigest()
    print(image_hash) 
    if expected_sha256 == image_hash:
        print("true")
        return True
    return False


def save_installer(installer_data):
    """Saves the VLC installer to a local directory.

    Args:
        installer_data (bytes): VLC installer file binary data

    Returns:
        str: Full path of the saved VLC installer file
    """

    # Hint: See example code in lab instructions entitled "Downloading a Binary File"

    file_path = r'C:\temp\vlc-3.0.21-win64'
        
    with open (file_path, 'wb') as file:
        file.write(installer_data)
        
    return file_path

def run_installer(installer_path):
    """Silently runs the VLC installer.

    Args:
        installer_path (str): Full path of the VLC installer file
    """    

    #See example code in lab instructions entitled "Running the VLC Installer"
    installer_path = r'C:\temp\vlc-3.0.21-win64'
    subprocess.run([installer_path,'/L=1033', '/S'])

    return
    
def delete_installer(installer_path):

    # Hint: See example code in lab instructions entitled "Running the VLC Installer"
    os.remove(installer_path= r'C:\temp\vlc-3.0.21-win64')
    return installer_path

if __name__ == '__main__':
    main()