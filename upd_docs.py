import os
import sys
import time
import curses
import shutil
import requests
import datetime
from pathlib import Path
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException



def auth_website(url, username, password):
    # Настройка драйвера Chrome
    service = Service(ChromeDriverManager().install())
    download_path = "C:\\Users\\t.sadykov\\Desktop\\Doc_shd"

    # Настройка параметров Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless") #фоновый режим драйвера
    prefs = {
        "download.default_directory": download_path,  # Установка директории для загрузки
        "download.prompt_for_download": False,  # Отключение запроса на подтверждение загрузки
        "download.directory_upgrade": True,  # Разрешение на обновление директории
        "plugins.always_open_pdf_externally": True,  # Открывать PDF-файлы в стороннем приложении
        "safebrowsing.enabled": True  # Включение безопасного просмотра
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=service, options=chrome_options) #запуск двоих настроенных драйверов
    driver2 = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Открываем указанный URL
        driver.get(url)
        
         # Открываем указанный URL
        driver2.get(url)
        
        # Подождем, пока страница загрузится
        driver.implicitly_wait(10)  # Ждем до 10 секунд

        # Пример: получаем заголовок страницы
        print("Заголовок страницы:", driver.title)
        
        # Найдите поле для ввода имени пользователя и введите его
        driver.find_element(By.ID, "id_username").send_keys(username)

        # Найдите поле для ввода пароля и введите его
        driver.find_element(By.ID, "id_password").send_keys(password) 

        # Найдите кнопку для отправки формы и нажмите на неё
        driver.find_element(By.ID, "loginFormButton").click()  # Замените на актуальный класс кнопки
        
        # Подождем, пока страница загрузится
        driver2.implicitly_wait(10)  # Ждем до 10 секунд
        
        # Найдите поле для ввода имени пользователя и введите его
        driver2.find_element(By.ID, "id_username").send_keys(username)

        # Найдите поле для ввода пароля и введите его
        driver2.find_element(By.ID, "id_password").send_keys(password) 

        # Найдите кнопку для отправки формы и нажмите на неё
        driver2.find_element(By.ID, "loginFormButton").click()  # Замените на актуальный класс кнопки
        
        # Проверяем, успешен ли вход
        try:
            # Проверка по элементу с определенным ID
            driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div/div[3]")
            driver2.find_element(By.XPATH, "/html/body/div[1]/header/div/div/div[3]")
            print("Вход выполнен успешно.")
            return driver, driver2  # Возвращаем драйвер для дальнейшего использования
        except:
            print("Неправильное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.")
            close_browser(driver)
            return None, None  # Неуспешный вход
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        close_browser(driver)
        return None, None # Неуспешный запуск

def close_browser(driver):
    if driver:
        driver.quit()  # Закрываем драйвер
        print("Браузер закрыт.")

def count_element(driver, by, value): # Метод для пересчета определенных элементов, также нужен чтоб if не выбрасывало ошибку при проверке существования элемента
    driver.implicitly_wait(5)
    elements = driver.find_elements(by, value)
    return len(elements) 
    
def convert_date_format(date_str): #перформатирование даты ('%d.%m.%y') в ('%d.%m.%Y'), если получает не дату то возвращает заглушку
    if (len(date_str) == 8 or len(date_str) == 10) and date_str[2] == '.' and date_str[5] == '.': # Проверка дата ли это
        day, month, year = date_str.split('.')# Вытаскиваем год для проверки
        print(f"{len(year)}")
        # Проверяем, если год состоит из двух цифр
        if len(year) == 2:
            year = '20' + year  # Добавляем "20" перед годом
        # Формируем новую строку в нужном формате
        return f"{day}.{month}.{year}"
    else:
        return "01.01.2099" # заглушка, документ скачается автоматически

def extract_version(element): # достаем версию из текста в элементе, для проверки выданных документов
    full_text = element.text
    
    # Удаляем подстроку "Версия документации " из текста
    prefix = "Версия документации "
    if full_text.startswith(prefix):
        version = full_text[len(prefix):]  # Извлекаем версию
        return version.strip()  # Убираем лишние пробелы
    else:
        return full_text.strip()
 
def choose_shd(stdscr,): # выбор СХД
    # Очищаем экран
    stdscr.clear()

    # Массив с текстовыми данными
    items = [
        "TATLIN Satellites",
        "TATLIN.ARCHIVE.L",
        "TATLIN.ARCHIVE.SE",
        "TATLIN.UNIFIED Gen1",
        "TATLIN.UNIFIED Gen2",
        "TATLIN.UNIFIED.SE",
    ]

    selected_items = []  # Массив для выбранных элементов
    current_selection = 0  # Индекс текущего выбора
    num_items = len(items)

    while True:
        stdscr.clear()  # Очищаем экран перед отрисовкой

        # Отображаем элементы
        for idx, item in enumerate(items):
            if idx == current_selection:
                stdscr.addstr(idx, 0, item, curses.A_REVERSE)  # Выделяем текущий выбор
            else:
                stdscr.addstr(idx, 0, item)

        stdscr.addstr(num_items + 1, 0, "Нажмите стрелки вверх вниз для указания, 'Enter' для выбора, 'Esc' для выхода с выбранными СХД.")  # Инструкция
        stdscr.addstr(num_items + 2, 0, "Выбранные элементы: " + ", ".join(selected_items))  # Отображаем выбранные элементы

        stdscr.refresh()  # Обновляем экран

        key = stdscr.getch()  # Получаем нажатую клавишу

        if key == curses.KEY_UP:  # Перемещение вверх
            current_selection = (current_selection - 1) % num_items
        elif key == curses.KEY_DOWN:  # Перемещение вниз
            current_selection = (current_selection + 1) % num_items
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Выбор элемента
            selected_item = items[current_selection]
            if selected_item not in selected_items:
                selected_items.append(selected_item)  # Добавляем выбранный элемент в массив
        elif key == 27:  # Код клавиши Esc
            break
    return selected_items
 
def click_element(driver, xpath): # навороченный клик по элементу, чтоб не было ошибок с динамическими элементами
    driver.implicitly_wait(5)
    attempts = 0
    while attempts < 3:  # Максимум 3 попытки
        try:
            element = driver.find_element(By.XPATH, xpath)
            element.click()
            return  # Успешно кликнули, выходим из функции
        except StaleElementReferenceException:
            attempts += 1
            time.sleep(1)  # Ждем перед повторной попыткой

def download_doc(driver, driver2, shd): # основной метод который обеспечивает скачивание документов
    try:
        work_dir = r"C:\Users\t.sadykov\Desktop\Doc_shd" # Путь куда будет все скачиваться
        
        for row in shd: #Начало цикла, проходимся по выбранным СХД из массива
            print(*row)
            shd_path = os.path.join(work_dir, row)
            
            if not os.path.exists(shd_path): # создание папки с именем СХД
                os.mkdir(shd_path)
                print(f'Директория {row} создана')
            else:
                print(f'Директория {row} уже существует')
                
            wait = WebDriverWait(driver, 5)  # Настройка неявных ожиданий до 5 секунд
            wait2 = WebDriverWait(driver2, 5)  
            driver.implicitly_wait(5)
            
            # Клик по элементу в навигации
            click_element(driver, '/html/body/nav/div[2]/ul/li[4]')
            
            for i in range (3): # здесь множество циклов чтоб скрипт просто не скопытился от рандомной ошибки, а также для прохода по всем документам всех версий
                try:
                    # Клик по разворачиванию списка
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='headlessui-listbox-button-:r3:']"))).click()
                    
                    # Клик по первому элементу в списке (чтоб избежать бага)
                    click_element(driver, '/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div[2]/ul/li[1]')
                    
                    # Клик по разворачиванию списка 
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-listbox-button-:r3:"]'))).click()
                    
                    # Клик по нужному элементу в списке
                    click_element(driver, f'//li[div[text()="{row}"]]')
                    
                    check_shd = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-listbox-button-:r3:"]')))
                    textcheck_shd = check_shd.text
                    
                    if not row == textcheck_shd: # Проверка что правильно выбран тип схд
                        continue
                  
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-listbox-button-:r5:"]'))).click() # Клик по разворачиванию выбора версий
                    
                    click_element(driver, '/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div[3]/ul/li[1]') # Клик по первому элементу в списке (чтоб избежать бага)
                    
                    time.sleep(0.5)
                    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-listbox-button-:r5:"]'))).click() # Клик по разворачиванию выбора версий
                    
                    time.sleep(0.5)
                    count_vers = count_element(driver, By.XPATH, f'/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div[3]/ul/li') # считаем сколько версий
                    
                    if count_vers == 0: # проверка для избежания бага 
                        continue
                    #print(f"{count_vers}")
            
                    break    
                except Exception as e:
                    continue
            
            for kekcount in range (0, count_element(driver, By.XPATH, f'/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div[3]/ul/li')): #проход по всем версиям
                
                for i in range (3):
                    try:
                        if kekcount != 0: #для правильной последовательности кликов
                            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-listbox-button-:r5:"]'))).click()
                            
                        time.sleep(0.5)
                        version = wait.until(EC.element_to_be_clickable((By.XPATH, f"/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div[3]/ul/li[{kekcount+1}]")))#определяем эелемент, вытаскиваем текст
                        vers_text = version.text
                        vers_path = os.path.join(shd_path, vers_text)#для создания папки куда будут скачаны все доки одной версии
                        
                        err_path = os.path.join(work_dir, "Без названия.pdf")#для определения неудачно скачанных файлов
                        err_down = os.path.join(work_dir, "Без названия.pdf.crdownload")
                        
                        err_path_v = os.path.join(vers_path, "Без названия.pdf")
                        err_down_v = os.path.join(vers_path, "Без названия.pdf.crdownload")
                            
                        if not os.path.exists(vers_path):#создание папки
                            os.mkdir(vers_path)
                            print(f'Директория {vers_text} создана')
                        else:
                            print(f'Директория {vers_text} уже существует')
              
                        # Клик по нужной версии
                        click_element(driver, f'/html/body/div[1]/div/div/div[2]/div/div[2]/div[2]/div[3]/ul/li[{kekcount+1}]')
                        
                        # Клик по кнопке "Найти"
                        click_element(driver, '//*[@id="technical-documentation-react-app"]/div/div[2]/div[2]/button')
                        
                        check_vers = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="technical-documentation-react-app"]/div/div[3]/div/div/div[1]/span/span')))#достаем текстовой элемент, показывающий версию документации
                        if extract_version(check_vers) != vers_text:#проверка что прогрузилось правильный набор доков
                            if kekcount == 0:# для правильной последовательности кликов
                                wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="headlessui-listbox-button-:r5:"]'))).click()
                            continue
                        print(f'Версия {extract_version(check_vers)} получена')
                        
                        
                        break
                    except Exception as e:
                        continue
            
                try:
                    empty = 0
                    count = 0
                    # Нахождение кнопки "downloads"
                    while empty < 1: #проход по всем выданным документам
                        count += 1 #счетчик для прохода по всем документам
                        
                        if count_element(driver, By.XPATH, f'//*[@id="technical-documentation-react-app"]/div/div[3]/div/div/div[2]/div[{count}]'):#если док по счетчику не найден, то значит что все доки скачаны. Сделано для скачки всех существующих доков.
                            
                            
                            if count_element(driver, By.XPATH, f'//*[@id="technical-documentation-react-app"]/div/div[3]/div/div/div[2]/div[{count}]/a'): #определение ссылки, в гостевом режиме у всех доков с пдф есть ссылка
                                id_text = "Что нового"
                                time.sleep(0.5)
                                element = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="technical-documentation-react-app"]/div/div[3]/div/div/div[2]/div[{count}]/a')))#фиксируем элемент с ссылкой 
                                href_value = element.get_attribute('href')#получаем ссылку
                                elementext = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#technical-documentation-react-app > div > div.ySxxArKf1qK_HfYaz97o > div > div > div.KlpbwaRDsfpsvEBFhzeL > div:nth-child({count}) > a > div > div.sOCBF7Gvv1TQbanb_z05")))
                                text_value = elementext.text #достаем текст для именования доков
                                
                                print(f'Документ {text_value}')
                                
                                try:
                                    print(f"Элемент имеет атрибут href: {href_value}")
                                        
                                    if not count_element(driver, By.CSS_SELECTOR, f'#technical-documentation-react-app > div > div.ySxxArKf1qK_HfYaz97o > div > div > div.KlpbwaRDsfpsvEBFhzeL > div:nth-child({count}) > div > div:nth-child(2)'): #проверка, есть ли html страница
                                        
                                        for i in range (3): # html страница не найдена, скачиваем док в любом случае
                                            try:
                                                # Находим элемент, на который нужно навести курсор
                                                element_to_hover_over = driver.find_element(By.CSS_SELECTOR, f'#technical-documentation-react-app > div > div.ySxxArKf1qK_HfYaz97o > div > div > div.KlpbwaRDsfpsvEBFhzeL > div:nth-child({count}) > div.BNjQwudEGNO2CRDTMGSO > div > svg')  # Укажите свой XPath или другой селектор

                                                # Создаем объект ActionChains
                                                actions = ActionChains(driver)

                                                # Наведение курсора на элемент
                                                actions.move_to_element(element_to_hover_over).perform()

                                                # Задержка, чтобы увидеть результат наведения
                                                time.sleep(0.2)
                                                    
                                                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#technical-documentation-react-app > div > div.ySxxArKf1qK_HfYaz97o > div > div > div.KlpbwaRDsfpsvEBFhzeL > div:nth-child({count}) > div.BNjQwudEGNO2CRDTMGSO > div > svg'))).click() #кликаем по возникающему элементу
                                                
                                                break
                                            except Exception as e: #при ошибке ждем и удаляем неудачно скачанные файлы
                                                time.sleep(5)
                                                
                                                if os.path.exists(err_path):
                                                    os.remove(err_path)
                                                    
                                                if os.path.exists(err_down):
                                                    os.remove(err_down)
                                                    
                                                continue
                                                
                                        if os.path.exists(err_path): # удаляем лишние файлы перед скачиванием которые могут помешать работе программы
                                                os.remove(err_path)
                            
                                        if os.path.exists(err_down):
                                            os.remove(err_down)
                                    
                                        if os.path.exists(err_path_v):
                                            os.remove(err_path_v)
                            
                                        if os.path.exists(err_down_v):
                                            os.remove(err_down_v)
                                        
                                        move_file(work_dir, vers_path, text_value) #ожидает скачанный файл, потом переносит его в сответствии версии и схд
                                            
                                        #print("1")   
                                    else: #в наличие есть html страница
                                        attempt = 0 
                                        
                                        while attempt < 3: #попытки узнать дату обновления в html странице, какдая попытка сопровождается обновлением страницы
                                            driver2.get(href_value) #передаем ссылку второму драйверу, ибо запара со вкладками стабильно валит скрипт на лопатки (драйвер вылетает)
                                            text_data = None
                                            
                                            if count_element(driver2, By.XPATH, f'//*[text()="{id_text}"]'): #проверка есть ли вкладка "Что нового", при отсутствии ставится заглушка, док скачивается автоматом
                                                #print("чек")
                                                click_element(driver2, f'//*[text()="{id_text}"]') #нажимаем на эту вкладку
                                                    
                                                for countcheck in range (0, 500): #ждем когда dom прогрузится, скрипт на js вычислит дату внутри dom 
                                                    try: #скрипт ищет первую попавшуюся дату с помощью селектора
                                                        host_element =  wait2.until( EC.presence_of_element_located((By.CSS_SELECTOR, '#technical-documentation-react-app > div > div.u4CEjQXlrSWsfDhQnGyl > div.XmU7TNbNbRPS2vWPwZVg > div'))) #находим эелмент с dom
                                                        text_data = driver2.execute_script(r'''
                                                                            const regex = /(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4}|\d{2})/;
                                                                            const walker = document.createTreeWalker(
                                                                                arguments[0].shadowRoot,
                                                                                NodeFilter.SHOW_ELEMENT,
                                                                                { 
                                                                                    acceptNode: node => regex.test(node.textContent.replace(/\s+/g, ' ')) 
                                                                                        ? NodeFilter.FILTER_ACCEPT 
                                                                                        : NodeFilter.FILTER_SKIP
                                                                                }
                                                                            );

                                                                            // Поиск в первом уровне shadow DOM
                                                                            let node = walker.nextNode();
                                                                            if (node) return node.textContent.match(regex)[0];

                                                                            // Рекурсивный поиск в nested shadow DOM
                                                                            const walkNested = root => {
                                                                                const nestedWalker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
                                                                                let current;
                                                                                while(current = nestedWalker.nextNode()) {
                                                                                    if(current.shadowRoot) {
                                                                                        const result = walkNested(current.shadowRoot);
                                                                                        if(result) return result;
                                                                                    }
                                                                                    if(regex.test(current.textContent)) {
                                                                                        return current.textContent.match(regex)[0];
                                                                                    }
                                                                                }
                                                                            };

                                                                            return walkNested(arguments[0].shadowRoot) || null;
                                                                            ''', host_element)
                                                                            
                                                        if text_data != None: #дата найдена, обрываем два цикла 
                                                            attempt += 3
                                                            break
                                                        elif countcheck > 499 &  attempt == 2: #дата не найдена, ставим заглушку вместо даты
                                                            text_data = "01.01.2099" #заглушка
                                                        
                                                    except Exception as e: #счетчик ошибок
                                                        print(f"Попытка: {countcheck}")  
                                                        
                                            else: #вкладка "Что нового" не найдено, ставим заглушку
                                                print("не чек")
                                                text_data = "01.01.2099" #заглушка
                                                break
                                                
                                            attempt += 1 # дата не найдега, обновляем страницу до 3
                                            
                                        file_path = os.path.join(vers_path, f"{text_value}.pdf") #присваиваем имя доку
                                        print(f"Проверка {text_data},{vers_path},{text_value}")
                                        
                                        if (not os.path.exists(file_path)) or check_upd(text_data, vers_path, text_value): #проверка что док надо обновлять из за устаревания, или из за того что файла самого нету
                                            #print("доходишь")
                                            
                                            for i in range (3):
                                                try:
                                                    # Находим элемент, на который нужно навести курсор
                                                    element_to_hover_over = driver.find_element(By.CSS_SELECTOR, f'#technical-documentation-react-app > div > div.ySxxArKf1qK_HfYaz97o > div > div > div.KlpbwaRDsfpsvEBFhzeL > div:nth-child({count}) > div > div:nth-child(2) > svg')  # Укажите свой XPath или другой селектор
                                                    
                                                    # Создаем объект ActionChains
                                                    actions = ActionChains(driver)
                                                    
                                                    # Наведение курсора на элемент
                                                    actions.move_to_element(element_to_hover_over).perform()

                                                    # Задержка, чтобы увидеть результат наведения (по желанию)
                                                    time.sleep(0.2)
                                                        
                                                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#technical-documentation-react-app > div > div.ySxxArKf1qK_HfYaz97o > div > div > div.KlpbwaRDsfpsvEBFhzeL > div:nth-child({count}) > div > div:nth-child(2) > svg'))).click()
                                                    
                                                    break
                                                except Exception as e: #при ошибке ждем и удаляем неудачно скачанные файлы
                                                    time.sleep(5)
                                                    
                                                    if os.path.exists(err_path):
                                                        os.remove(err_path)
                                                        
                                                    if os.path.exists(err_down):
                                                        os.remove(err_down)
                                                        
                                                    continue
                                                    
                                            if os.path.exists(err_path): # удаляем лишние файлы перед скачиванием которые могут помешать работе программы
                                                os.remove(err_path)
                            
                                            if os.path.exists(err_down):
                                                os.remove(err_down)
                                    
                                            if os.path.exists(err_path_v):
                                                os.remove(err_path_v)
                            
                                            if os.path.exists(err_down_v):
                                                os.remove(err_down_v)
                                                
                                            move_file(work_dir, vers_path, text_value) #ожидает скачанный файл, потом переносит его в сответствии версии и схд
                                                  
                                            print("2")
                                            
                                except Exception as e:
                                    print(f"Произошла ошибка1: {e}") 
                            else:
                                print("Элемент не имеет атрибута href.") #если не имеет ссылки то не имеет pdf - пропуск
                        else: 
                            empty += 1
                            
                except Exception as e:
                    print(f"Произошла ошибка2: {e}")
                
    except Exception as e:
        print(f"Произошла ошибка3: {e}")

def move_file(source_dir, target_dir, text_name): #отправка дока в нужную директорию с нужным именем
    # Определяем имена файлов
    original_file_name = "Без названия.pdf"
    new_file_name = f"{text_name}.pdf"
        
    # Полные пути к файлам
    original_file_path = os.path.join(source_dir, original_file_name)
    new_file_path = os.path.join(target_dir, new_file_name)
    existing_file_path = os.path.join(target_dir, f"{text_name}.pdf")
        
    # Установка времени ожидания
    wait_time = 5 * 60  # 5 минут в секундах
    start_time = time.time()

    # Ожидание появления файла
    while not os.path.exists(original_file_path):
        elapsed_time = time.time() - start_time
        if elapsed_time > wait_time:
            print(f"Файл '{text_name}' не найден в течение 5 минут. Завершение ожидания.")
            return  # Выход из функции, если файл не найден за 5 минут
        time.sleep(2)
        
    # Проверяем, существует ли файл "Без названия.pdf" в исходной директории
    if os.path.exists(original_file_path):
        # Удаляем существующий файл с именем {text_name}.pdf, если он существует
        if os.path.exists(existing_file_path):
            os.remove(existing_file_path)
            print(f'Файл {existing_file_path} был удален.')
            
        # Перемещаем и переименовываем файл
        shutil.move(original_file_path, new_file_path)
        print(f'Файл {original_file_name} перемещен и переименован в {new_file_name}.')
    else:
        print(f'Файл {original_file_name} не найден в директории {source_dir}.')
        
def check_upd (date_string, source_file_path, text_name): #сравнение даты обновления в html странице с датой изменения соответствующего файла, заглушка автоматом проходит
    date_string = convert_date_format(date_string)
    # Преобразуем строку с датой в объект datetime
    date_from_string = datetime.datetime.strptime(date_string, "%d.%m.%Y")
        
    existing_file_path = os.path.join(source_file_path, f"{text_name}.pdf")
        
    # Получаем время последнего изменения файла
    mtime = os.path.getmtime(existing_file_path)

    # Преобразуем временную метку в объект datetime
    last_modified_time = datetime.datetime.fromtimestamp(mtime)

    # Сравниваем даты
    if date_from_string > last_modified_time:
        print(f"Дата {date_from_string.strftime('%d.%m.%Y')} новее, чем дата последнего изменения файла {last_modified_time.strftime('%d.%m.%Y')}.")
        return True 
    elif date_from_string < last_modified_time:
        print(f"Дата {last_modified_time.strftime('%d.%m.%Y')} новее, чем дата {date_from_string.strftime('%d.%m.%Y')}.")
        return False
    else:
        print("Даты равны.")
        return False
    
def main():
    url = "https://servicepartner.yadro.com/"  # Укажите URL сайта
    driver = None
    driver2 = None
    shd = curses.wrapper(choose_shd) # выюор схд

    while True:
        # Запросите у пользователя имя пользователя и пароль
        username = input("Введите ваше имя пользователя: ")
        password = getpass("Введите ваш пароль: ")  # Ввод пароля без отображения
        
        driver, driver2 = auth_website(url, username, password)
        if driver:
            break  # Выход из цикла, если вход успешен
            
    
    download_doc(driver, driver2, shd) 
    
    # Ожидание команды для завершения программы
    try:
        input("Нажмите Enter, чтобы закрыть программу...")
    except KeyboardInterrupt:
        print("\nЗавершение программы...")
    
    close_browser(driver)  # Закрываем браузер перед завершением

if __name__ == "__main__":
    try:
        main()
    finally:
        input("Нажми на любую кнопку чтоб продолжить...")
