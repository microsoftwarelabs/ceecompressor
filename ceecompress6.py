import zipfile
import os
import tempfile
import pyzipper

def compress_file(file_path, output_file):
    if not os.path.exists(file_path):

        print(f"Error: File '{file_path}' does not exist.")

        return

    # rest of the function
    output_file = output_file + '.cee'  # Add.cee extension to output file
    temp_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    with zipfile.ZipFile(temp_file.name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.write(file_path, os.path.basename(file_path))

    for _ in range(56):  # Loop compression 56 more times
        with zipfile.ZipFile(temp_file.name, mode="r") as input_archive:
            temp_file_tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
            with zipfile.ZipFile(temp_file_tmp.name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output_archive:
                for item in input_archive.infolist():
                    output_archive.writestr(item, input_archive.read(item.filename))
        os.replace(temp_file_tmp.name, temp_file.name)

    with open(output_file, 'wb') as f:
        with open(temp_file.name, 'rb') as tmp_file:
            f.write(tmp_file.read())
    os.remove(temp_file.name)

def compress_files(directory, output_file):
    output_file = output_file + '.cee'  # Add.cee extension to output file
    temp_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    with zipfile.ZipFile(temp_file.name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                archive.write(file_path, arcname)

    for _ in range(56):  # Loop compression 56 more times
        with zipfile.ZipFile(temp_file.name, mode="r") as input_archive:
            temp_file_tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
            with zipfile.ZipFile(temp_file_tmp.name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output_archive:
                for item in input_archive.infolist():
                    output_archive.writestr(item, input_archive.read(item.filename))
        os.replace(temp_file_tmp.name, temp_file.name)

    with open(output_file, 'wb') as f:
        with open(temp_file.name, 'rb') as tmp_file:
            f.write(tmp_file.read())
    os.remove(temp_file.name)

def unzip_file(file_path):
    with pyzipper.AESZipFile(file_path, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as archive:
        archive.extractall(path=os.path.splitext(file_path)[0])  # Specify the extraction path

def view_file_without_unzipping(file_path, file_to_view):
    with pyzipper.AESZipFile(file_path, 'r', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as archive:
        if file_to_view in archive.namelist():  # Check if the file exists in the archive
            with archive.open(file_to_view) as f:
                print(f.read().decode())
        else:
            print(f"File '{file_to_view}' not found in the archive.")

# Example usage:
file_path = "../files/file.txt"
output_file = "compressed_file"
compress_file(file_path, output_file)

directory = "sparkylinux-7.4-x86"
output_file = "compressed_files"
compress_files(directory, output_file)

unzip_file(output_file + '.cee')  # Unzip the file

view_file_without_unzipping(output_file + '.cee', 'file_to_view.txt')  # View a file without unzipping
