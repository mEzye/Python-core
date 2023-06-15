import os
import shutil
unknown_exts = set()

def normalize(filename):
    translit_table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh',
        'з': 'z', 'i': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ь': '', 'ю': 'yu', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 
        'Ж': 'Zh', 'З': 'Z', 'І': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
        'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ь': '', 'Ю': 'Yu', 'Я': 'Ya'
    }

    result = ''
    for char in filename:
        if char.isalpha() and char.isascii():
            result += char
        elif char in translit_table:
            result += translit_table[char]
        else:
            result += '_'
    return result

def process_folder(folder_path):
    image_exts = ('JPEG', 'PNG', 'JPG', 'SVG')
    video_exts = ('AVI', 'MP4', 'MOV', 'MKV')
    document_exts = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio_exts = ('MP3', 'OGG', 'WAV', 'AMR')
    archive_exts = ('ZIP', 'GZ', 'TAR')
    known_extensions = set()  # Змінна для збереження відомих розширень

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            filename, ext = os.path.splitext(file)
            ext = ext[1:].upper()

            if ext in image_exts:
                dest_folder = 'images'
                known_extensions.add(ext)  # Додати розширення до відомих
            elif ext in video_exts:
                dest_folder = 'video'
                known_extensions.add(ext)
            elif ext in document_exts:
                dest_folder = 'documents'
                known_extensions.add(ext)
            elif ext in audio_exts:
                dest_folder = 'audio'
                known_extensions.add(ext)
            elif ext in archive_exts:
                dest_folder = 'archives'
                dest_subfolder = normalize(filename)
                dest_folder = os.path.join(dest_folder, dest_subfolder)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.unpack_archive(os.path.join(root, file), dest_folder)
                continue
            else:
                unknown_exts.add(ext)
                continue

            dest_folder = os.path.join(folder_path, dest_folder)
            os.makedirs(dest_folder, exist_ok=True)
            shutil.move(os.path.join(root, file), os.path.join(dest_folder, file))

    return known_extensions

# Введення шляху до папки
target_folder = input("Введіть шлях до папки: ")
known_extensions = process_folder(target_folder)

print('Known extensions:')
print(', '.join(known_extensions))
print()
print('Unknown extensions:')
print(', '.join(unknown_exts))
