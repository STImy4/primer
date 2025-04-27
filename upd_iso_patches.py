import os
import shutil

def copy_files_from_network(source_dest_pairs):
    for source_dir, destination_dir in source_dest_pairs.items():
        # Проверка существования папки в куда надо все положить, при отсутствии оной создает
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Проверка доступа к источнику (для сетевых дисков), если нету переходим к следующим папкам
        if not os.path.exists(source_dir):
            print(f"Сетевой источник не найден: {source_dir}")
            continue

        # Список всех файлов в исходной папке
        source_files = set()

        # Проход по всем файлам исходной папки и их запоминание
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_dir)
                destination_file_path = os.path.join(destination_dir, relative_path, file)

                # Добавляем файл в список всех файлов в исходной папке
                source_files.add(os.path.relpath(source_file_path, source_dir))

                # Проверка, существует ли папка назначения, если нет - создаем
                if not os.path.exists(os.path.dirname(destination_file_path)):
                    os.makedirs(os.path.dirname(destination_file_path))

                # Если файл не существует или он новее, копируем его
                if not os.path.exists(destination_file_path) or \
                   os.path.getmtime(source_file_path) > os.path.getmtime(destination_file_path):
                    try:
                        shutil.copy2(source_file_path, destination_file_path)
                        print(f"Скопирован: {source_file_path} -> {destination_file_path}")
                    except Exception as e:
                        print(f"Ошибка при копировании файла {source_file_path}: {e}")

        # Удаляем файлы в папке скачивания,если их нет в списке исходной папки
        for root, dirs, files in os.walk(destination_dir):
            for file in files:
                destination_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(destination_file_path, destination_dir)

                # Проверка, есть ли файл в списке
                if relative_path not in source_files:
                    try:
                        os.remove(destination_file_path)
                        print(f"Удален: {destination_file_path}")
                    except Exception as e:
                        print(f"Ошибка при удалении файла {destination_file_path}: {e}")

if __name__ == "__main__":
    # в source_dest_pairs пишешь из какой папки хочешь скопировать и в какую папку хочешь вставить по такому шаблону-> r"С:\путь\исходной_папки\откуда\все_скопировать": r"D:\путь\куда_все_скинуть"
    # не забывай про запятые между шаблонами!!! копирует ВСЁ что найдет по исходному пути (кроме того что уже есть в папке скачивания)!!!
    # скрипт удаляет все файлы которых нет в исходной папке, поэтому в конце пути, куда копируете, ставте пустую папку(либо то что требует обновления из исходной папки)!!!!!!
    # требования просты - права на чтение откуда качаешь и права на чтение и запись в куда качаешь, также требует скачивание питона без дополнительных библиотек
    # работает с двумя разными дисками, работает с сетевыми дисками, качает выборочно то что новое
    # если ничего не написало, значит у вас актуальные данные из исходной папки
    source_dest_pairs = {
        r"J:\База знаний\Tatlin Unified\База знаний Tatlin Unified\Образы\TATLIN.UNIFIED.Gen1": r"C:\Users\t.sadykov\Desktop\ISO_files\TATLIN.UNIFIED.Gen1",
        r"J:\База знаний\Tatlin Unified\База знаний Tatlin Unified\Образы\TATLIN.UNIFIED.Gen2": r"C:\Users\t.sadykov\Desktop\ISO_files\TATLIN.UNIFIED.Gen2",
        r"J:\Сервис\Группа Unified\Файлы для обновлений": r"C:\Users\t.sadykov\Desktop\Updates_files",
        r"J:\База знаний\Tatlin Unified\База знаний Tatlin Unified\Образы\TATLIN.UNIFIED.SE": r"C:\Users\t.sadykov\Desktop\ISO_files\TATLIN.UNIFIED.SE"
    }

    copy_files_from_network(source_dest_pairs)
    input("Нажми на любую кнопку чтоб продолждить...")
    