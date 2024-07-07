import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox
from PySide6.QtCore import QTimer
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PySide6.QtCore import QTimer, QCoreApplication

opt=Options(); opt.add_experimental_option("debuggerAddress","localhost:8989"); driver=webdriver.Chrome(executable_path="C:\\DominData\\chromedriver.exe",chrome_options=opt)   #DO ZMIANY
try: driver.switch_to.window(driver.window_handles[0])
except: time.sleep(0.1)
url = driver.current_url; print ("Current website: " +str(url))

def Hit_points():
    life = driver.find_element(By.XPATH,'//*[@id="header_values_hp_percent"]').text.replace("%","")
    life = int(life)
    return life

def Expedition_enemy(enemy_number):
    
    to_expedition = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_expedition"]/a')
    driver.execute_script("$(arguments[0]).click();", to_expedition)
    try: enemy_block = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[1]/div[2]/div')
    except:
        if enemy_number == 1:
            enemy = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[1]/div[2]/button')
            try: enemy_block = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[1]/div[2]/div')
            except: time.sleep(0.1)
        if enemy_number == 2:                   
            enemy = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[2]/div[2]/button')
        if enemy_number == 3:
            enemy = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[3]/div[2]/button')
        if enemy_number == 4:
            enemy = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[4]/div[2]/button')
        time.sleep(1)
        driver.execute_script("$(arguments[0]).click();", enemy);  time.sleep(1.5)
    try: 
        gold_expedition = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[1]').text.replace(".","")
        matches = re.findall(r"([\d:,.]+)", gold_expedition)
        gold_expedition = matches[1]
        gold_expedition = int(gold_expedition)
    except: time.sleep(0.1)
    try: 
        xp_expedition = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[2]').text
        matches = re.findall(r"([\d:,.]+)", xp_expedition)
        xp_expedition = matches[0]
        xp_expedition = int(xp_expedition)
    except: time.sleep(0.1)
    try: 
        honour_expedition = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[3]').text.replace(".","")
        matches = [int(s) for s in re.findall(r"([\d:,.]+)", honour_expedition)]
        honour_expedition = int(matches[0])
    except: time.sleep(0.1)
    return  gold_expedition, xp_expedition, honour_expedition

def Dungeons():
    to_dungeons = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_dungeon"]/a')
    driver.execute_script("$(arguments[0]).click();", to_dungeons); time.sleep(1)
    try:
        normal_dungeons = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/form/table/tbody/tr/td[1]/input')
        advanced_dungeons = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div/form/table/tbody/tr/td[2]/input')
        driver.execute_script("$(arguments[0]).click();", advanced_dungeons); time.sleep(1)
    except: time.sleep(0)
    dungeon_enemies = ['//*[@id="content"]/div[2]/div/img[1]','//*[@id="content"]/div[2]/div/img[2]','//*[@id="content"]/div[2]/div/img[3]','//*[@id="content"]/div[2]/div/img[4]','//*[@id="content"]/div[2]/div/img[5]','//*[@id="content"]/div[2]/div/img[6]','//*[@id="content"]/div[2]/div/img[7]','//*[@id="content"]/div[2]/div/img[8]','//*[@id="content"]/div[2]/div/img[9]','//*[@id="content"]/div[2]/div/img[10]','//*[@id="content"]/div[2]/div/img[11]','//*[@id="content"]/div[2]/div/img[12]','//*[@id="content"]/div[2]/div/img[13]','//*[@id="content"]/div[2]/div/img[14]','//*[@id="content"]/div[2]/div/img[15]']
    try: enemy_block = driver.find_element(By.XPATH,'//*[@id="content"]/div[1]/div/div/form/input')                   
    except:
        try:
            for i in range(0,14):      
                try:
                    enemy = driver.find_element(By.XPATH,dungeon_enemies[i])
                    driver.execute_script("$(arguments[0]).click();", enemy); time.sleep(0.5)
                except: time.sleep(0.1)
        except: time.sleep(0.1)

def Eat(player):
    try:
        view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[1]/a[1]')
        driver.execute_script("$(arguments[0]).click();", view);time.sleep(1)
        try:
            page2 = driver.find_element(By.XPATH,'//*[@id="inventory_nav"]/a[2]')
            driver.execute_script("$(arguments[0]).click();", page2)
        except: time.sleep(0)
        try:
            player_name = driver.find_element(By.XPATH,'//*[@id="content"]/table/tbody/tr/td[1]/div[1]/div[1]').text
            player_hp = driver.find_element(By.XPATH,'//*[@id="char_leben"]').text
            if player_name == player and player_hp != "100 %":
                try:
                    eating = driver.find_element(By.XPATH,'//*[@id="inv"]/div[1]') 
                    driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", eating)
                    time.sleep(2)
                except: Food_packages()
            elif player_name == player and player_hp == "100 %":
                try:
                    first = driver.find_element(By.XPATH,'//*[@id="char"]/div[17]/div')
                    driver.execute_script("$(arguments[0]).click();", first);time.sleep(1)
                    player_name = driver.find_element(By.XPATH,'//*[@id="content"]/table/tbody/tr/td[1]/div[1]/div[1]').text
                    player_hp = driver.find_element(By.XPATH,'//*[@id="char_leben"]').text
                    if player_name == player:
                        try:
                            eating = driver.find_element(By.XPATH,'//*[@id="inv"]/div[1]') 
                            driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", eating)
                            time.sleep(2)
                        except: Food_packages()
                except:
                    time.sleep(0.1)
            else:
                try:
                    second = driver.find_element(By.XPATH,'//*[@id="char"]/div[14]/div')
                    driver.execute_script("$(arguments[0]).click();", second);time.sleep(1)
                    try:
                        eating = driver.find_element(By.XPATH,'//*[@id="inv"]/div[1]') 
                        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", eating)
                        time.sleep(2)
                    except: Food_packages()
                except: time.sleep(0)     
        except: time.sleep(0.1)
    except: time.sleep(2)

def Eat_before_10():
    try:
        view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[1]/a[1]')
        driver.execute_script("$(arguments[0]).click();", view);time.sleep(1)
    except:time.sleep(0.1)
    try:
        page2 = driver.find_element(By.XPATH,'//*[@id="inventory_nav"]/a[2]')
        driver.execute_script("$(arguments[0]).click();", page2)
    except: time.sleep(0)    
    try:
        eating = driver.find_element(By.XPATH,'//*[@id="inv"]/div[1]') 
        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", eating)
        time.sleep(2)
    except: Food_packages()
    
def Food_packages():
    try:
        food_packages_count = 15
        packages_view = driver.find_element(By.XPATH,'//*[@id="menue_packages"]')
        driver.execute_script("$(arguments[0]).click();", packages_view); time.sleep(1)
        item_type = driver.find_element(By.XPATH,'//*[@id="mainnav"]/li/table/tbody/tr/td/a[10]')# <--DO WPISANIA ŚCIEŻKA IKONKI Z JEDZENIEM(ADDON)
        driver.execute_script("$(arguments[0]).click();", item_type); time.sleep(0.5)
        try:
            last_packages = driver.find_element(By.XPATH,'//*[@id="content"]/article/div[3]/div/div/a[1]')
            driver.execute_script("$(arguments[0]).click();", last_packages); time.sleep(1)
        except: time.sleep(0.1)
        try:
            second_backpack = driver.find_element(By.XPATH,'//*[@id="inventory_nav"]/a[2]')
            driver.execute_script("$(arguments[0]).click();", second_backpack); time.sleep(0.5)
        except: time.sleep(0.1)
        i=0
        for i in range(1,food_packages_count):
            try:
                food = driver.find_element(By.XPATH,'//*[@id="packages"]/div/div[2]/div') 
                driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", food)
                time.sleep(0.5)
            except: time.sleep(0.1)  
    except: time.sleep(0.1)

def Arena():
    to_arena = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_arena"]/a')
    driver.execute_script("$(arguments[0]).click();", to_arena); time.sleep(1)
    try: prov_check = driver.find_element(By.XPATH,'//*[@id="content"]/article/form/input').get_attribute("value")
    except: 
        provinciarum = driver.find_element(By.XPATH,'//*[@id="mainnav"]/li/table/tbody/tr/td[2]/a')
        driver.execute_script("$(arguments[0]).click();", provinciarum); time.sleep(1)
    enemy = driver.find_element(By.XPATH,'//*[@id="own2"]/table/tbody/tr[2]/td[4]/div')
    driver.execute_script("$(arguments[0]).click();", enemy); time.sleep(1)
    Reattack()
    try:
        fight_winner = driver.find_element(By.XPATH,'//*[@id="reportHeader"]/table/tbody/tr/td[2]').text
        regex = r'\b\w+\b'
        matches = re.findall(regex,fight_winner)
        fight_winner = matches[1]
        return fight_winner
    except: time.sleep(0.1)

def Arena_server(previous_arena_winner):
    to_arena = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_arena"]/a')
    driver.execute_script("$(arguments[0]).click();", to_arena); time.sleep(1)
    try: arena_check = driver.find_element(By.XPATH,'//*[@id="content"]/article/aside[1]/h2').get_attribute("value")
    except: 
        arena_server = driver.find_element(By.XPATH,'//*[@id="mainnav"]/li/table/tbody/tr/td[1]/a')
        driver.execute_script("$(arguments[0]).click();", arena_server); time.sleep(1)
    if previous_arena_winner == 1:
        enemy = driver.find_element(By.XPATH,'//*[@id="content"]/article/aside[2]/section/table/tbody/tr[5]/td[2]/div')
        driver.execute_script("$(arguments[0]).click();", enemy); time.sleep(1)
    else: 
        enemy = driver.find_element(By.XPATH,'//*[@id="content"]/article/aside[2]/section/table/tbody/tr[4]/td[2]/div')
        driver.execute_script("$(arguments[0]).click();", enemy); time.sleep(1)
    Reattack()
    try:
        fight_winner = driver.find_element(By.XPATH,'//*[@id="reportHeader"]/table/tbody/tr/td[2]').text
        regex = r'\b\w+\b'
        matches = re.findall(regex,fight_winner)
        fight_winner = matches[1]
        return fight_winner
    except: time.sleep(0.1)

def Arena_report():
    try: 
        gold_arena = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[1]').text.replace(".","")
        matches = re.findall(r"([\d:,.]+)", gold_arena)
        gold_arena = matches[1]
        gold_arena = int(gold_arena)
    except: time.sleep(0.1)
    try: 
        xp_arena = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[2]').text
        matches = re.findall(r"([\d:,.]+)", xp_arena)
        xp_arena = matches[0]
        xp_arena = int(xp_arena)
        return gold_arena,xp_arena
    except: time.sleep(0.1)

def Circus():
    attacked = 0
    enemies_list = ['Dodupyzaur', 'MaxsimusMike', 'TifoOosi', 'Kleopatra', 'Engineer', 'xxx', 'Grzenia', 'BrahaT4', 'TheEnd', 'Marecki889', 'Kutotward', 'DeeJay', 'Pigmej', 'Drax85', 'Talias', 'risky23', 'Gekon', 'Grindheim', 'Jasiu', 'PeRSoN', 'Julian', 'Markus', 'LiW3r', 'Tits', 'JeffreyDahmer', 'destroymator', 'BandytaJeden', 'PepAK', 'PaterAetius', 'Missclick', 'Wrexex', 'Wojownik28', 'Borsuczek', 'Sami', 'TusioGod', 'Semper_Fidelis', 'Dawid', 'Piachu']
    enemies = ['//*[@id="own3"]/table/tbody/tr[2]/td[1]/a','//*[@id="own3"]/table/tbody/tr[3]/td[1]/a','//*[@id="own3"]/table/tbody/tr[4]/td[1]/a','//*[@id="own3"]/table/tbody/tr[5]/td[1]/a','//*[@id="own3"]/table/tbody/tr[6]/td[1]/a']
    enemies_click = ['//*[@id="own3"]/table/tbody/tr[2]/td[4]/div','//*[@id="own3"]/table/tbody/tr[3]/td[4]/div','//*[@id="own3"]/table/tbody/tr[4]/td[4]/div','//*[@id="own3"]/table/tbody/tr[5]/td[4]/div','//*[@id="own3"]/table/tbody/tr[6]/td[4]/div']
    elements = len(enemies_list)
    to_arena = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_ct"]/a')
    driver.execute_script("$(arguments[0]).click();", to_arena); time.sleep(1)
    try: ct_check = driver.find_element(By.XPATH,'//*[@id="content"]/article/form/input').get_attribute("value")
    except:
        provinciarum = driver.find_element(By.XPATH,'//*[@id="mainnav"]/li/table/tbody/tr/td[4]/a')
        driver.execute_script("$(arguments[0]).click();", provinciarum); time.sleep(1)
    try:
        for i in range (0,5):
            enemy_check = enemies[i]
            enemy_click = enemies_click[i]
            enemy = driver.find_element(By.XPATH,enemy_check).text
            for j in range (elements):
                enemy_from_list = enemies_list[j]
                if enemy_from_list == enemy:
                    enemy_click = driver.find_element(By.XPATH,enemy_click)
                    attacked = 1
                    driver.execute_script("$(arguments[0]).click();", enemy_click);  time.sleep(1.5)
                    Reattack()
            i = i + 1
    except: time.sleep(0.01)
    if attacked == 0:
        try:
            enemy_click = driver.find_element(By.XPATH,'//*[@id="own3"]/table/tbody/tr[2]/td[4]/div')
            driver.execute_script("$(arguments[0]).click();", enemy_click);  time.sleep(1.5)
        except: time.sleep(0.01)
    Reattack()
    try:
        fight_winner = driver.find_element(By.XPATH,'//*[@id="reportHeader"]/table/tbody/tr/td[2]').text
        regex = r'\b\w+\b'
        matches = re.findall(regex,fight_winner)
        fight_winner = matches[1]
        return fight_winner
    except: time.sleep(0.1)

def Circus_report():
    try: 
        gold_circus = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[1]').text.replace(".","")
        matches = re.findall(r"([\d:,.]+)", gold_circus)
        gold_circus = matches[1]
        gold_circus = int(gold_circus)
    except: time.sleep(0.1)
    try: 
        xp_circus = driver.find_element(By.XPATH,'//*[@id="content"]/div[3]/section/table/tbody/tr[1]/td/p[2]').text
        matches = re.findall(r"([\d:,.]+)", xp_circus)
        xp_circus = matches[0]
        xp_circus = int(xp_circus)
        return gold_circus,xp_circus
    except: time.sleep(0.1)

def Reattack():
    try:
        message = driver.find_element(By.XPATH,'//*[@id="header_bod"]').text
        message_button = driver.find_element(By.XPATH,'//*[@id="linkbod"]')
        if message == "Zaatakować pomimo tego?":
            driver.execute_script("$(arguments[0]).click();", message_button); time.sleep(3.5)
    except: time.sleep(0.01)

def Quests(quest_counter,arena, circus):
    all_quests = ['//*[@id="content"]/div[1]/div/div[2]/div[2]','//*[@id="content"]/div[1]/div/div[3]/div[2]','//*[@id="content"]/div[1]/div/div[4]/div[2]','//*[@id="content"]/div[1]/div/div[5]/div[2]','//*[@id="content"]/div[1]/div/div[6]/div[2]','//*[@id="content"]/div[1]/div/div[7]/div[2]','//*[@id="content"]/div[1]/div/div[8]/div[2]','//*[@id="content"]/div[1]/div/div[9]/div[2]','//*[@id="content"]/div[1]/div/div[10]/div[2]','//*[@id="content"]/div[1]/div/div[11]/div[2]']   
    buttons = ['//*[@id="content"]/div[1]/div/div[2]/a','//*[@id="content"]/div[1]/div/div[3]/a','//*[@id="content"]/div[1]/div/div[4]/a','//*[@id="content"]/div[1]/div/div[5]/a','//*[@id="content"]/div[1]/div/div[6]/a','//*[@id="content"]/div[1]/div/div[7]/a','//*[@id="content"]/div[1]/div/div[8]/a','//*[@id="content"]/div[1]/div/div[9]/a','//*[@id="content"]/div[1]/div/div[10]/a','//*[@id="content"]/div[1]/div/div[11]/a']
    quests_gold = ['//*[@id="content"]/div[1]/div/div[2]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[3]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[4]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[5]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[6]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[7]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[8]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[9]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[10]/div[3]/div[1]','//*[@id="content"]/div[1]/div/div[11]/div[3]/div[1]']
    quests_honor = ['//*[@id="content"]/div[1]/div/div[2]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[3]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[4]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[5]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[6]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[7]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[8]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[9]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[10]/div[3]/div[4]','//*[@id="content"]/div[1]/div/div[11]/div[3]/div[4]']
    quests_exp = ['//*[@id="content"]/div[1]/div/div[2]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[3]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[4]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[5]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[6]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[7]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[8]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[9]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[10]/div[3]/div[5]','//*[@id="content"]/div[1]/div/div[11]/div[3]/div[5]']
    if (arena == 0 and circus == 0) or (arena == 2 and circus == 0):
        task = ["Pokonaj 5 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 6 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 7 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 8 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 9 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 10 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Circus Turma: Wygraj kilka razy z rzędu (3) z gladiatorami, od których możesz otrzymać złoto","Pokonaj 5 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 6 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 7 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 8 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 9 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 10 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 11 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 12 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 13 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 14 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 15 przeciwników podczas ekspedycji, w lochach lub na arenie","Znajdź 3 przedmiotów podczas ekspedycji lub w lochach","Znajdź 4 przedmiotów podczas ekspedycji lub w lochach","Znajdź 5 przedmiotów podczas ekspedycji lub w lochach","Znajdź 6 przedmiotów podczas ekspedycji lub w lochach","Znajdź 7 przedmiotów podczas ekspedycji lub w lochach","Znajdź 8 przedmiotów podczas ekspedycji lub w lochach"]
    if arena == 0 and circus == 1:
        task = ["Pokonaj 5 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 6 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 7 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 8 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 9 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 10 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Circus Turma: Wygraj kilka razy z rzędu (3) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (4) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (5) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (6) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (7) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj walki (4), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (5), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (6), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (7), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (8), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (9), awansując na arenie lub walcz na arenie Circus Provinciarum","Pokonaj 5 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 6 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 7 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 8 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 9 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 10 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 11 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 12 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 13 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 14 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 15 przeciwników podczas ekspedycji, w lochach lub na arenie","Circus Turma: Wygraj (3) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (4) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (5) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (6) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (7) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (8) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (9) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka walk (3) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (4) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (5) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (6) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (7) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (8) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Znajdź 3 przedmiotów podczas ekspedycji lub w lochach","Znajdź 4 przedmiotów podczas ekspedycji lub w lochach","Znajdź 5 przedmiotów podczas ekspedycji lub w lochach","Znajdź 6 przedmiotów podczas ekspedycji lub w lochach","Znajdź 7 przedmiotów podczas ekspedycji lub w lochach","Znajdź 8 przedmiotów podczas ekspedycji lub w lochach","Circus Turma: Wygraj walki (3), awansując na arenie lub walcz na arenie Circus Provinciarum"]
    if arena == 1 and circus == 1:
        task = ["Pokonaj 5 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 6 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 7 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 8 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 9 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Pokonaj 10 przeciwników z rzędu podczas ekspedycji, w lochach lub na arenie","Circus Turma: Wygraj kilka razy z rzędu (3) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (4) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (5) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (6) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka razy z rzędu (7) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj walki (4), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (5), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (6), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (7), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (8), awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj walki (9), awansując na arenie lub walcz na arenie Circus Provinciarum","Pokonaj 5 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 6 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 7 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 8 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 9 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 10 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 11 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 12 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 13 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 14 przeciwników podczas ekspedycji, w lochach lub na arenie","Pokonaj 15 przeciwników podczas ekspedycji, w lochach lub na arenie","Circus Turma: Wygraj (3) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (4) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (5) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (6) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (7) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (8) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj (9) przeciwko gladiatorom, od których możesz otrzymać złoto","Circus Turma: Wygraj kilka walk (3) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (4) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (5) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (6) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (7) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Circus Turma: Wygraj kilka walk (8) z rzędu, awansując na arenie lub walcz na arenie Circus Provinciarum","Znajdź 3 przedmiotów podczas ekspedycji lub w lochach","Znajdź 4 przedmiotów podczas ekspedycji lub w lochach","Znajdź 5 przedmiotów podczas ekspedycji lub w lochach","Znajdź 6 przedmiotów podczas ekspedycji lub w lochach","Znajdź 7 przedmiotów podczas ekspedycji lub w lochach","Znajdź 8 przedmiotów podczas ekspedycji lub w lochach","Arena: Zaatakuj zwycięsko przeciwników (3), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (4), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (5), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (6), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (7), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (8), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (9), od których możesz otrzymać złoto","Arena: Zaatakuj zwycięsko przeciwników (10), od których możesz otrzymać złoto","Arena: Wygraj kilka walk (3) z rzędu, awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj kilka walk (4) z rzędu, awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj kilka walk (5) z rzędu, awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj kilka walk (6) z rzędu, awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj kilka walk (7) z rzędu, awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (3), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (4), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (5), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (6), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (7), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (8), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj walki (9), awansując na arenie lub walcz na Arenie Provinciarum","Arena: Wygraj kilka razy z rzędu (3) z gladiatorami, od których możesz otrzymać złoto","Arena: Wygraj kilka razy z rzędu (4) z gladiatorami, od których możesz otrzymać złoto","Arena: Wygraj kilka razy z rzędu (5) z gladiatorami, od których możesz otrzymać złoto","Arena: Wygraj kilka razy z rzędu (6) z gladiatorami, od których możesz otrzymać złoto","Arena: Wygraj kilka razy z rzędu (7) z gladiatorami, od których możesz otrzymać złoto","Arena: Wygraj kilka razy z rzędu (8) z gladiatorami, od których możesz otrzymać złoto","Circus Turma: Wygraj walki (3), awansując na arenie lub walcz na arenie Circus Provinciarum"]
    try:
        gold_quest = 0
        honor_quest = 0
        exp_quest = 0
        panteon = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[2]/a[1]')
        driver.execute_script("$(arguments[0]).click();", panteon); time.sleep(1)
        for i in range(0,10):
            quest = all_quests[i]
            button = buttons[i]
            reward_gold = quests_gold[i]
            reward_honor = quests_honor[i]
            reward_exp = quests_exp[i]
            quest_1 = driver.find_element(By.XPATH,quest).text
            try:
                buttonstr = driver.find_element(By.XPATH,button).get_attribute("title")
                button_click = driver.find_element(By.XPATH,button)
                button_name = str(buttonstr)
                reward_gold_str = driver.find_element(By.XPATH,reward_gold).text.replace(".","")
                reward_gold = int(reward_gold_str)
                try:
                    reward_exp_str = driver.find_element(By.XPATH,reward_exp).text.replace(".","")
                    reward_exp = int(reward_exp_str)
                except: time.sleep(0.01)
                reward_honor_str = driver.find_element(By.XPATH,reward_honor).text.replace(".","")
                reward_honor = int(reward_honor_str)
                if button_name == "Zakończ zadanie":
                    driver.execute_script("$(arguments[0]).click();", button_click); time.sleep(1)
                    gold_quest = gold_quest + reward_gold
                    exp_quest = exp_quest + reward_exp
                    honor_quest = honor_quest + reward_honor
                    quest_counter = quest_counter + 1
                if button_name == "Zacznij zadanie od początku":
                    driver.execute_script("$(arguments[0]).click();", button_click); time.sleep(1)
                for i in task:
                    if quest_1 == i:
                        if button_name == "Przyjmij zadanie":
                            driver.execute_script("$(arguments[0]).click();", button_click); time.sleep(1)   
            except: time.sleep(0)
        new_quests = driver.find_element(By.XPATH,'//*[@id="quest_footer_reroll"]/input')
        driver.execute_script("$(arguments[0]).click();", new_quests); time.sleep(1)
        return gold_quest, quest_counter, honor_quest, exp_quest
    except: time.sleep(1)

def Pack_gold(money):
    market_packages = ['//*[@id="market_item_table"]/tbody/tr[2]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[3]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[4]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[5]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[6]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[7]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[8]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[9]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[10]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[11]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[12]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[13]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[14]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[15]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[16]/td[1]/div','//*[@id="market_item_table"]/tbody/tr[17]/td[1]/div']
    market_prices = ['//*[@id="market_item_table"]/tbody/tr[2]/td[3]','//*[@id="market_item_table"]/tbody/tr[3]/td[3]','//*[@id="market_item_table"]/tbody/tr[4]/td[3]','//*[@id="market_item_table"]/tbody/tr[5]/td[3]','//*[@id="market_item_table"]/tbody/tr[6]/td[3]','//*[@id="market_item_table"]/tbody/tr[7]/td[3]','//*[@id="market_item_table"]/tbody/tr[8]/td[3]','//*[@id="market_item_table"]/tbody/tr[9]/td[3]','//*[@id="market_item_table"]/tbody/tr[10]/td[3]','//*[@id="market_item_table"]/tbody/tr[11]/td[3]','//*[@id="market_item_table"]/tbody/tr[12]/td[3]','//*[@id="market_item_table"]/tbody/tr[13]/td[3]','//*[@id="market_item_table"]/tbody/tr[14]/td[3]','//*[@id="market_item_table"]/tbody/tr[15]/td[3]','//*[@id="market_item_table"]/tbody/tr[16]/td[3]','//*[@id="market_item_table"]/tbody/tr[17]/td[3]']
    market_buy_packages = ['//*[@id="market_item_table"]/tbody/tr[2]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[3]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[4]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[5]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[6]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[7]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[8]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[9]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[10]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[11]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[12]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[13]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[14]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[15]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[16]/td[6]/input','//*[@id="market_item_table"]/tbody/tr[17]/td[6]/input']
    search_package = ['//*[@id="packages"]/div[1]/div[2]/div','//*[@id="packages"]/div[2]/div[2]/div','//*[@id="packages"]/div[3]/div[2]/div']
    high_value = 0
    if money > 1110000:
        value_to_buy = 1000000; high_value = 1
    elif money < 1110000 and money > 600000:
        value_to_buy = 500000; high_value = 1
    elif money < 600000 and money > 380000:
        value_to_buy = 300000
    elif money < 380000 and money > 250000:
        value_to_buy = 200000
    elif money < 250000 and money > 130000:
        value_to_buy = 100000
    try:
        guild_view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[3]/a[1]')
        driver.execute_script("$(arguments[0]).click();", guild_view); time.sleep(2)
        market_view = driver.find_element(By.XPATH,'//*[@id="guild_market_div"]')
        driver.execute_script("$(arguments[0]).click();", market_view); time.sleep(2)
        sort_by_price = driver.find_element(By.XPATH,'//*[@id="market_item_table"]/tbody/tr[1]/th[3]/a')
        driver.execute_script("$(arguments[0]).click();", sort_by_price); time.sleep(2)
        if high_value == 1:
            sort_by_price = driver.find_element(By.XPATH,'//*[@id="market_item_table"]/tbody/tr[1]/th[3]/a')
            driver.execute_script("$(arguments[0]).click();", sort_by_price); time.sleep(2)
        for i in range(0,12):
            package = market_packages[i]
            package_price = market_prices[i]
            buy_package = market_buy_packages[i]
            package_price_str = driver.find_element(By.XPATH,package_price).text.replace(".","")
            package_price = int(package_price_str)
            buy_package_str = driver.find_element(By.XPATH,buy_package).get_attribute("value")
            if package_price == value_to_buy and buy_package_str == "Kup":
                bought_package_str = driver.find_element(By.XPATH,package).get_attribute("class")
                print(bought_package_str,"for",package_price_str,buy_package_str)
                buy_package = driver.find_element(By.XPATH,buy_package)
                driver.execute_script("$(arguments[0]).click();", buy_package); time.sleep(5)
                packages_view = driver.find_element(By.XPATH,'//*[@id="menue_packages"]')
                driver.execute_script("$(arguments[0]).click();", packages_view); time.sleep(5)
                page1 = driver.find_element(By.XPATH,'//*[@id="inventory_nav"]/a[1]')
                driver.execute_script("$(arguments[0]).click();", page1); time.sleep(2)
                i=0
                for i in range(0,3):
                    search_packages = search_package[i]
                    package_str = driver.find_element(By.XPATH,search_packages).get_attribute("class")
                    all_words = package_str.split()
                    first_word = all_words[0]
                    if first_word == bought_package_str:
                        package = driver.find_element(By.XPATH,search_packages) 
                        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", package); time.sleep(5)
                        guild_view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[3]/a[1]')
                        driver.execute_script("$(arguments[0]).click();", guild_view); time.sleep(2)
                        market_view = driver.find_element(By.XPATH,'//*[@id="guild_market_div"]')
                        driver.execute_script("$(arguments[0]).click();", market_view); time.sleep(2)
                        item_click = driver.find_element(By.XPATH,'//*[@id="inv"]/div')
                        driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('dblclick'))", item_click); time.sleep(5)
                        price = driver.find_element(By.CSS_SELECTOR,'#preis')
                        price.clear(); time.sleep(1)
                        price = driver.find_element(By.CSS_SELECTOR,'#preis')
                        driver.execute_script("arguments[0].value = arguments[1];", price, value_to_buy); time.sleep(1)
                        sell_click = driver.find_element(By.XPATH,'//*[@id="sellForm"]/input')
                        driver.execute_script("$(arguments[0]).click();", sell_click); time.sleep(2)       
    except: time.sleep(1)

def To_hades_after_healing():
    try:
        world = driver.find_element(By.XPATH,'//*[@id="submenuhead1"]/div[2]/a')
        driver.execute_script("$(arguments[0]).click();", world); time.sleep(1.5)
    except: time.sleep(0.1)
    try:
        oldman = driver.find_element(By.XPATH,'//*[@id="submenu2"]/a[1]')
        driver.execute_script("$(arguments[0]).click();", oldman); time.sleep(1.5)
    except: time.sleep(0.1)

def To_hades(player):
    try:
        try:
            world = driver.find_element(By.XPATH,'//*[@id="submenuhead1"]/div[2]/a')
            driver.execute_script("$(arguments[0]).click();", world); time.sleep(0.5)
        except: time.sleep(0.1)
        try:
            oldman = driver.find_element(By.XPATH,'//*[@id="submenu2"]/a[1]')
            driver.execute_script("$(arguments[0]).click();", oldman); time.sleep(1.5)
            hades_link_str = driver.find_element(By.XPATH,'//*[@id="content"]/div[4]/a').text
            if hades_link_str == "Nie możesz jeszcze powrócić do Hadesu. Poczekaj trochę dłużej i pozwól swojej duszy odpocząć, by znowu mogła zmierzyć się przepastnym mrokiem.":
                print ("nie mozesz wejsc do hadesu")
            if hades_link_str == "Na pewno chcesz odkrywać zaświaty? Jest to zupełnie nowy wymiar - pełen śmierci i zagłady.":
                life = Hit_points(); 
                if life < 95:
                    Eat(player)
                    To_hades_after_healing()
                life = Hit_points();
                if life > 95:
                    hades_enabled = 1
                    hades_enter = driver.find_element(By.XPATH,'//*[@id="content"]/div[4]/a')
                    driver.execute_script("$(arguments[0]).click();", hades_enter); time.sleep(5)
                    print("1. Wchodzę w wybór trudności hadesu")
                    hades_enter_easy = driver.find_element(By.XPATH,'//*[@id="enterForm"]/section/input[2]')
                    driver.execute_script("$(arguments[0]).click();", hades_enter_easy); time.sleep(5)
                    print("2. Wchodze w hades łatwy")
                    return hades_enabled
        except: time.sleep(0.1)
    except: time.sleep(0.1)

def Reconnect():
    driver.refresh;time.sleep(10)
    login = driver.find_element(By.XPATH,'//*[@id="joinGame"]/button');login.click(); time.sleep(10)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.minimize_window()
    url = driver.current_url; print ("Current website: " +str(url))
    player_view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[1]/a[1]')
    driver.execute_script("$(arguments[0]).click();", player_view);  time.sleep(1.5)

def Hades_expedition():
    time.sleep(2)
    To_expedition = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_expedition"]/a')
    driver.execute_script("$(arguments[0]).click();", To_expedition); time.sleep(2)
    try:
        Hades_enemy = driver.find_element(By.XPATH,'//*[@id="expedition_button4"]')
        driver.execute_script("$(arguments[0]).click();", Hades_enemy); time.sleep(1)
    except: time.sleep(0.001)
    try:
        Hades_enemy = driver.find_element(By.XPATH,'//*[@id="expedition_button3"]')
        driver.execute_script("$(arguments[0]).click();", Hades_enemy); time.sleep(1)
    except: time.sleep(0.001)
    try:
        Hades_enemy = driver.find_element(By.XPATH,'//*[@id="expedition_button2"]')
        driver.execute_script("$(arguments[0]).click();", Hades_enemy); time.sleep(1)
    except: time.sleep(0.001)
    try:
        Hades_enemy = driver.find_element(By.XPATH,'//*[@id="expedition_button1"]')
        driver.execute_script("$(arguments[0]).click();", Hades_enemy); time.sleep(1)
    except: time.sleep(0.001)

def Medics ():
    guild_enter = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[3]/a[1]')
    driver.execute_script("$(arguments[0]).click();", guild_enter); time.sleep(1.5)
    villa_enter = driver.find_element(By.XPATH,'//*[@id="doctor_div"]')
    driver.execute_script("$(arguments[0]).click();", villa_enter); time.sleep(1.5)
    try:
        life = Hit_points(); 
        if life < 40:
            healer = driver.find_element(By.XPATH,'//*[@id="guild_medicus_heal"]/section/table/tbody/tr[1]/td[2]/a')
            driver.execute_script("$(arguments[0]).click();", healer); time.sleep(1.5)
    except: time.sleep(0.001)
    try:
        life = Hit_points(); 
        if life < 40:
            healer = driver.find_element(By.XPATH,'//*[@id="guild_medicus_heal"]/section/table/tbody/tr[2]/td[2]/a')
            driver.execute_script("$(arguments[0]).click();", healer); time.sleep(1.5)
    except: time.sleep(0.001)
    try:
        life = Hit_points(); 
        if life < 40:
            healer = driver.find_element(By.XPATH,'//*[@id="guild_medicus_heal"]/section/table/tbody/tr[3]/td[2]/a')
            driver.execute_script("$(arguments[0]).click();", healer); time.sleep(1.5)
    except: time.sleep(0.001)
    try:
        life = Hit_points(); 
        if life < 40:
            healer = driver.find_element(By.XPATH,'//*[@id="guild_medicus_heal"]/section/table/tbody/tr[4]/td[2]/a')
            driver.execute_script("$(arguments[0]).click();", healer); time.sleep(1.5)
    except: time.sleep(0.001)
    time.sleep(10)
class BotController(QMainWindow,QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gladiatus Bot")
        self.setGeometry(100, 100, 400, 400)
#Nazwa postaci
        self.label = QLabel("Nazwa postaci", self)
        self.label.setGeometry(20, 20, 100, 25)
        self.playername_input = QLineEdit(self)
        self.playername_input.setGeometry(100, 20, 60, 25)
#Wyprawa
        self.label = QLabel("Paczkowanie", self)
        self.label.setGeometry(20, 50, 100, 30)
        self.checkbox_packager = QCheckBox(self)
        self.checkbox_packager.setGeometry(95, 52, 100, 30)
        self.checkbox_packager.stateChanged.connect(lambda state: self.checkbox_packager_state_changed(state))  # Użycie funkcji lambda
        self.checked_packager = False
#Lochy
        self.label = QLabel("Lochy", self)
        self.label.setGeometry(120, 50, 100, 30)
        self.checkbox_dungeon = QCheckBox(self)
        self.checkbox_dungeon.setGeometry(160, 52, 100, 30)
        self.checkbox_dungeon.stateChanged.connect(lambda state: self.checkbox_dungeon_state_changed(state))  # Użycie funkcji lambda
        self.checked_dungeon = False
#Hades
        self.label = QLabel("Hades", self)
        self.label.setGeometry(190, 50, 100, 30)
        self.checkbox_hades = QCheckBox(self)
        self.checkbox_hades.setGeometry(225, 52, 100, 30)
        self.checkbox_hades.stateChanged.connect(lambda state: self.checkbox_hades_state_changed(state))  # Użycie funkcji lambda
        self.checked_hades = False
#Event
        self.label = QLabel("Event", self)
        self.label.setGeometry(260, 50, 100, 30)
        self.checkbox_event = QCheckBox(self)
        self.checkbox_event.setGeometry(295, 52, 100, 30)
        self.checkbox_event.stateChanged.connect(lambda state: self.checkbox_event_state_changed(state))  # Użycie funkcji lambda
        self.checked_event = False
#Arena
        self.label = QLabel("Arena", self)
        self.label.setGeometry(20, 80, 100, 30)
        self.arena_input = QLineEdit(self)
        self.arena_input.setGeometry(65, 80, 30, 30)
#Circus Turma
        self.label = QLabel("Circus", self)
        self.label.setGeometry(110, 80, 100, 30)
        self.circus_input = QLineEdit(self)
        self.circus_input.setGeometry(160, 80, 30, 30)
#Wyprawa przeciwnik
        self.label = QLabel("Przeciwnik", self)
        self.label.setGeometry(200, 80, 100, 30)
        self.expeditionenemy_input = QLineEdit(self)
        self.expeditionenemy_input.setGeometry(260, 80, 30, 30)
#Przerwa
        self.label = QLabel("Przerwa w grze na", self)
        self.label.setGeometry(20, 300, 100, 25)
        self.break_input = QLineEdit(self)
        self.break_input.setGeometry(120, 300, 30, 25)
        self.label = QLabel("minut, gdy 0 wypraw", self)
        self.label.setGeometry(152, 300, 120, 25)
#Start
        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(50, 130, 150, 30)
        self.start_button.clicked.connect(self.start_logging)
#Stop
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(220, 130, 150, 30)
        self.stop_button.clicked.connect(self.stop_logging)
#Labels
        self.counter_label = QLabel("Licznik obrotów: 0", self)
        self.counter_label.setGeometry(20, 150, 200, 30)
        self.label = QLabel("Statystyki:", self)
        self.label.setGeometry(20, 170, 200, 30)
        self.expedition_label = QLabel("Wyprawa", self)
        self.expedition_label.setGeometry(20, 190, 200, 30)
        self.quest_label = QLabel("Zadania", self)
        self.quest_label.setGeometry(20, 210, 200, 30)
        self.circus_label = QLabel("Turma", self)
        self.circus_label.setGeometry(20, 230, 200, 30)
        self.arena_label = QLabel("Arena", self)
        self.arena_label.setGeometry(20, 250, 200, 30)
        self.label = QLabel("RAZEM", self)
        self.label.setGeometry(20, 270, 200, 30)
        self.label = QLabel("Gold", self)
        self.label.setGeometry(120, 170, 200, 30)
        self.label = QLabel("Exp", self)
        self.label.setGeometry(180, 170, 200, 30)
        self.label = QLabel("Honor", self)
        self.label.setGeometry(240, 170, 200, 30)
        self.gold1_label = QLabel("0", self)
        self.gold1_label.setGeometry(120, 190, 200, 30)
        self.gold2_label = QLabel("0", self)
        self.gold2_label.setGeometry(120, 210, 200, 30)
        self.gold3_label = QLabel("0", self)
        self.gold3_label.setGeometry(120, 230, 200, 30)
        self.gold4_label = QLabel("0", self)
        self.gold4_label.setGeometry(120, 250, 200, 30)
        self.goldt_label = QLabel("0", self)
        self.goldt_label.setGeometry(120, 270, 200, 30)
        self.exp1_label = QLabel("0", self)
        self.exp1_label.setGeometry(180, 190, 200, 30)
        self.exp2_label = QLabel("0", self)
        self.exp2_label.setGeometry(180, 210, 200, 30)
        self.exp3_label = QLabel("0", self)
        self.exp3_label.setGeometry(180, 230, 200, 30)
        self.exp4_label = QLabel("0", self)
        self.exp4_label.setGeometry(180, 250, 200, 30)
        self.expt_label = QLabel("0", self)
        self.expt_label.setGeometry(180, 270, 200, 30)
        self.honour1_label = QLabel("0", self)
        self.honour1_label.setGeometry(240, 190, 200, 30)
        self.honour2_label = QLabel("0", self)
        self.honour2_label.setGeometry(240, 210, 200, 30)
        self.honour3_label = QLabel("-", self)
        self.honour3_label.setGeometry(240, 230, 200, 30)
        self.honour4_label = QLabel("-", self)
        self.honour4_label.setGeometry(240, 250, 200, 30)
        self.honourt_label = QLabel("0", self)
        self.honourt_label.setGeometry(240, 270, 200, 30)

        self.data_counter = 0; self.quest_timer = 10; self.timer = 0; self.event_timer = 149; self.packager_counter = 19; self.hades_timer = 200; self.counter_break = 0; self.time_to_break = 0; self.in_hades_timer = 0
        self.expedition_hades = 1; self.dungeon_hades = 1; self.arena_hades = 1; self.hades_enabled = 0; self.in_hades = 0
        self.total_gold_expedition = 0; self.total_xp_expedition = 0; self.expedition_counter = 0; self.total_honour_expedition = 0
        self.total_gold_quest = 0; self.quest_counter = 0; self.total_honour_quest = 0; self.total_xp_quest = 0
        self.total_gold_arena = 0; self.total_xp_arena = 0; self.arena_counter = 0; self.arena_win_counter = 0; self.arena_previous_winner = 1
        self.total_gold_circus = 0; self.total_xp_circus = 0; self.circus_counter = 0; self.circus_win_counter = 0
        self.total_gold = 0; self.total_xp = 0; self.total_honour = 0

        self.logging_timer = QTimer(self)
        self.logging_timer.timeout.connect(self.log_data)
        self.is_logging = False

    def checkbox_event_state_changed(self, state):
        if state == 2:  # 2 oznacza stan zaznaczony
            self.checked_event = 1
        else:
            self.checked_event = 0

    def checkbox_hades_state_changed(self, state):
        if state == 2:  # 2 oznacza stan zaznaczony
            self.checked_hades = 1
        else:
            self.checked_hades = 0
    
    def checkbox_packager_state_changed(self, state):
        if state == 2:  # 2 oznacza stan zaznaczony
            self.checked_packager = 1
        else:
            self.checked_packager = 0

    def checkbox_dungeon_state_changed(self, state):
        if state == 2:  # 2 oznacza stan zaznaczony
            self.checked_dungeon = 1
        else:
            self.checked_dungeon = 0

    def start_logging(self):
        self.is_logging = True
        self.logging_timer.start(1000)  # Uruchamiamy timer, zapisywanie co 1000ms (1 sekunda)

    def stop_logging(self):
        self.is_logging = False
        self.logging_timer.stop()  # Zatrzymujemy timer

    def log_data(self):
        if self.is_logging:
            player = self.playername_input.text()
            if player == '':
                player = "Marco_Reus"
            window_name = "Gladiatus Bot - " + player
            self.setWindowTitle(window_name)
            if self.checked_hades == 1: self.checking_hades = 1
            else: self.checking_hades = 0
            enemy_number = self.expeditionenemy_input.text()
            if enemy_number == '1' or enemy_number == '2' or enemy_number == '3' or enemy_number == '4':
                enemy_number = int(enemy_number)
            else: enemy_number = 0
            dungeon = int(self.checked_dungeon)
            arena = self.arena_input.text()
            if arena == '0' or arena == '1' or arena == '2':
                arena = int(arena)
            else: arena = 0
            circus = self.circus_input.text()
            if circus == '0' or circus == '1':
                circus = int(circus)
            else: circus = 0
            event = int(self.checked_event)
            break_input = self.break_input.text()
            if break_input == '':
                break_time = 0
            else: 
                break_time = int(break_input)* 60
            self.data_counter += 1
            self.counter_label.setText(f"Licznik obrotów: {self.data_counter}")
            self.expedition_label.setText(f"Wyprawa ({self.expedition_counter})")
            self.quest_label.setText(f"Zadania ({self.quest_counter})")
            self.circus_label.setText(f"Turma {self.circus_win_counter}/{self.circus_counter} ")
            self.arena_label.setText(f"Arena  {self.arena_win_counter}/{self.arena_counter} ")
            self.gold1_label.setText(f" {self.total_gold_expedition}")
            self.gold2_label.setText(f" {self.total_gold_quest}")
            self.gold3_label.setText(f" {self.total_gold_circus}")
            self.gold4_label.setText(f" {self.total_gold_arena}")
            self.goldt_label.setText(f" {self.total_gold}")
            self.exp1_label.setText(f" {self.total_xp_expedition}")
            self.exp2_label.setText(f" {self.total_xp_quest}")
            self.exp3_label.setText(f" {self.total_xp_circus}")
            self.exp4_label.setText(f" {self.total_xp_arena}")
            self.expt_label.setText(f" {self.total_xp}")
            self.honour1_label.setText(f" {self.total_honour_expedition}")
            self.honour2_label.setText(f" {self.total_honour_quest}")
            self.honourt_label.setText(f" {self.total_honour}")
#OTHER WINDOWS
            try:
                bonus = driver.find_element(By.XPATH,'//*[@id="linkLoginBonus"]')
                driver.execute_script("$(arguments[0]).click();", bonus); time.sleep(0.5)
            except: time.sleep(0.001)
            try:
                level_up = driver.find_element(By.XPATH,'//*[@id="linknotification"]')
                driver.execute_script("$(arguments[0]).click();", level_up); time.sleep(0.5)
            except: time.sleep(0.001)
#PACK GOLD
            money = driver.find_element(By.XPATH,'//*[@id="sstat_gold_val"]').text.replace(".","")
            money = int(money)
            if money > 130000 and self.packager_counter > 20 and self.checked_packager == 1:
                self.packager_counter = 0
                Pack_gold(money)
#QUESTS
            try:
                timer_pantheon = driver.find_element(By.XPATH,'//*[@id="QuestTime"]').text
                if (timer_pantheon == "(Nowe)" or self.quest_timer > 30) or (timer_pantheon == "(Pełny)" and self.quest_timer > 10):
                    self.quest_timer = 0
                    gold_quest,self.quest_counter, honor_quest, exp_quest = Quests(self.quest_counter,arena,circus)
                    self.total_gold_quest = self.total_gold_quest + gold_quest   
                    self.total_gold = self.total_gold + gold_quest
                    gold_quest = 0
                    self.total_xp_quest = self.total_xp_quest + exp_quest
                    self.total_xp = self.total_xp + exp_quest
                    exp_quest = 0
                    self.total_honour_quest = self.total_honour_quest + honor_quest
                    self.total_honour = self.total_honour + honor_quest
                    honor_quest = 0
                    time.sleep(random.uniform(0.5,1))
            except: time.sleep(0.001)
#EXPEDITION
            try:
                if (enemy_number > 0 and enemy_number < 5) and self.expedition_hades == 1:
                    check_expedition = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_text_expedition"]').text
                    life = Hit_points(); 
                    if life > 40:
                        if (check_expedition) == "Na wyprawę": 
                            time.sleep(random.uniform(1.0, 2.0))
                            gold_expedition,xp_expedition,honour_expedition = Expedition_enemy(enemy_number)
                            self.total_gold_expedition = self.total_gold_expedition + gold_expedition
                            self.total_gold = self.total_gold + gold_expedition
                            gold_expedition = 0
                            self.total_xp_expedition = self.total_xp_expedition + xp_expedition
                            self.total_xp = self.total_xp + xp_expedition
                            xp_expedition = 0
                            self.total_honour_expedition = self.total_honour_expedition + honour_expedition
                            self.total_honour = self.total_honour + honour_expedition
                            honour_expedition = 0
                            self.expedition_counter = self.expedition_counter + 1
                            time.sleep(random.uniform(1.5,2.5))
                    else:
                        try:    
                            Eat(player)
                        except: time.sleep(0.001)
            except: time.sleep(0.001)
#DUNGEON
            try:
                if dungeon == 1 and self.dungeon_hades == 1:
                    check_dungeons = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_text_dungeon"]').text
                    if check_dungeons == "Do lochów" and dungeon == 1:
                        time.sleep(random.uniform(1.0, 2.0))
                        Dungeons()
                        time.sleep(random.uniform(1.5, 2.5))
            except: time.sleep(0.001)
#ARENA PROVINCIARUM     
            try:
                if arena == 1 and self.arena_hades == 1:
                    check_arena = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_text_arena"]').text
                    life = Hit_points()
                    if life > 40:
                        if (check_arena) == "Do areny":
                            time.sleep(random.uniform(1.0, 2.0))
                            fight_winner = Arena()
                            time.sleep(random.uniform(1.5,2.5))
                            t = time.localtime()
                            current_time = time.strftime("%H:%M:%S", t)
                            if fight_winner == player:
                                gold_arena, xp_arena = Arena_report()
                                self.arena_counter = self.arena_counter + 1
                                self.arena_win_counter = self.arena_win_counter + 1
                                self.total_gold_arena = self.total_gold_arena + gold_arena
                                self.total_gold = self.total_gold + gold_arena
                                gold_arena = 0
                                self.total_xp_arena = self.total_xp_arena + xp_arena
                                self.total_xp = self.total_xp + xp_arena
                                xp_arena = 0
                                time.sleep(random.uniform(1.5,2.5))
                            else: 
                                self.arena_counter += 1        
                    else:
                        try:    
                            Eat(player)
                        except: time.sleep(0.001)
            except: time.sleep(0.001)
#ARENA LOCAL SERVER      
            try:
                arena_place = driver.find_element(By.XPATH,'//*[@id="arenaPlace"]').text
                arena_place = int(arena_place)
                if arena_place > 10:
                    if arena == 2 and self.arena_hades == 1:
                        check_arena = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_text_arena"]').text
                        life = Hit_points()
                        if life > 40:
                            if (check_arena) == "Do areny":
                                if self.arena_previous_winner == 1:
                                    previous_arena_winner = 1
                                else:
                                    previous_arena_winner = 0
                                time.sleep(random.uniform(1.0, 2.0))
                                fight_winner = Arena_server(previous_arena_winner)
                                time.sleep(random.uniform(1.5,2.5))
                                t = time.localtime()
                                current_time = time.strftime("%H:%M:%S", t)
                                if fight_winner == player:
                                    self.arena_previous_winner == 1
                                    gold_arena, xp_arena = Arena_report()
                                    self.arena_counter = self.arena_counter + 1
                                    self.arena_win_counter = self.arena_win_counter + 1
                                    self.total_gold_arena = self.total_gold_arena + gold_arena
                                    self.total_gold = self.total_gold + gold_arena
                                    gold_arena = 0
                                    self.total_xp_arena = self.total_xp_arena + xp_arena
                                    self.total_xp = self.total_xp + xp_arena
                                    xp_arena = 0
                                    time.sleep(random.uniform(1.5,2.5))
                                else: 
                                    self.arena_counter += 1        
                                    self.arena_previous_winner == 0
                        else:
                            try:    
                                Eat(player)
                            except: time.sleep(0.001)
            except: time.sleep(0.001)
#CIRCUS TURMA
            try:
                if circus == 1:
                    check_circus = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_text_ct"]').text
                    if (check_circus) == "Do Circus Turma":
                        time.sleep(random.uniform(1.0, 2.0))
                        fight_winner = Circus()
                        time.sleep(random.uniform(1.5,2.5))
                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        if fight_winner == player:
                            gold_circus, xp_circus = Circus_report()
                            self.circus_counter = self.circus_counter + 1
                            self.circus_win_counter = self.circus_win_counter + 1
                            self.total_gold_circus = self.total_gold_circus + gold_circus
                            self.total_gold = self.total_gold + gold_circus
                            gold_circus = 0
                            self.total_xp_circus = self.total_xp_circus + xp_circus
                            self.total_xp = self.total_xp + xp_circus
                            xp_circus = 0
                            time.sleep(random.uniform(1.5,2.5))
                        else: 
                            self.circus_counter += 1
            except: time.sleep(0.001)      
#Check Hades
            if self.checking_hades == 1:
                try:    
                    if self.hades_timer > 200 and self.in_hades == 0 :
                        self.hades_timer = 0
                        hades_enabled = To_hades(player)
                        print("3. sprawdzam Hades enabled:", hades_enabled)
                        if hades_enabled == 1:
                            self.hades_enabled = 1
                            self.in_hades = 1    
                        print("4. sprawdzam self.hades_enabled:", self.hades_enabled, "oraz self.in_hades:", self.in_hades)
                except: time.sleep(0.1) 
#Travel Hades
            if self.in_hades == 1 and self.in_hades_timer > 30:
                print("Sprawdzenie co 30 obrotów zmiennych self.in_hades", self.in_hades)
                self.in_hades_timer = 0
                try: 
                    Reconnect()
                    print("5. Pierwszy reconnect udany")
                except: 
                    time.sleep(0.001)
                    print("5. Pierwszy reconnect nieudany")
                try:
                    driver.refresh(); time.sleep(3)
                    print("6. Odświeżenie sterownika udane")
                except:
                    time.sleep(0.0001)
                    print("6. Odświeżenie sterownika nieudane")
                try: 
                    Reconnect()
                    print("7. Drugi reconnect udany")
                except: 
                    time.sleep(0.001)
                    print("7. Drugi reconnect nieudany")
                try:
                    view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[1]/a[1]')
                    driver.execute_script("$(arguments[0]).click();", view); time.sleep(2)
                except: time.sleep(0.1)
                print("hades enabled = ",self.hades_enabled, "in hades = ", self.in_hades)
#Hades
            try:
                quit_hades_button = driver.find_element(By.XPATH,'//*[@id="submenu2"]/a[1]').text
                if quit_hades_button == "Opuść Hades":
                    self.in_hades = 1
            except: time.sleep(0.1)
            if self.in_hades == 1:
                self.expedition_hades = 0; self.dungeon_hades = 0; self.arena_hades = 0   
                try:
                    hades_points = driver.find_element(By.XPATH,'//*[@id="expeditionpoints_value_pointmax"]').text
                    if (hades_points) == '18':
                        life = Hit_points(); 
                        if life > 40:
                            check_expedition = driver.find_element(By.XPATH,'//*[@id="cooldown_bar_text_expedition"]').text
                            if check_expedition == "Na wyprawę":
                                Hades_expedition()    
                        else:
                            Medics()
                        try:
                            check_finish_hades = driver.find_element(By.XPATH,'//*[@id="header_notification"]').text
                            if check_finish_hades == "Dokonało się!":
                                self.hades_enabled = 0; self.expedition_hades = 1; self.dungeon_hades = 1; self.arena_hades = 1; self.in_hades = 0
                        except: time.sleep(0.01)
                        try:
                            hades_points = driver.find_element(By.XPATH,'//*[@id="expeditionpoints_value_pointmax"]').text
                            if (hades_points) != '18':
                                self.hades_enabled = 0; self.expedition_hades = 1; self.dungeon_hades = 1; self.arena_hades = 1; self.in_hades = 0
                        except: time.sleep(0.01)
                    else: 
                        Reconnect()
                except: time.sleep(0.001)        
#EVENT
            try:
                if self.event_timer > 150 and event == 1 :
                    self.event_timer = 0
                    to_event = driver.find_element(By.XPATH,'//*[@id="submenuhead1"]/div[2]/a')
                    driver.execute_script("$(arguments[0]).click();", to_event); time.sleep(2)
                    to_event = driver.find_element(By.XPATH,'//*[@id="submenu2"]/a[9]')
                    driver.execute_script("$(arguments[0]).click();", to_event); time.sleep(2)
                    event_count = driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[2]/p[2]').text
                    matches = re.findall(r"([\d:,.]+)", event_count)
                    event_count = matches[1]
                    event_count = int(event_count)
                    if event_count > 0:
                        event_enemy = driver.find_element(By.XPATH,'//*[@id="expedition_list"]/div[3]/div[2]/button')
                        driver.execute_script("$(arguments[0]).click();", event_enemy); time.sleep(2)
                    elif event_count == 0:
                        event = 0
            except: time.sleep(0.001)
#TIMERS
            self.quest_timer += 1
            self.timer += 1
            self.event_timer += 1
            self.packager_counter += 1
            self.hades_timer += 1
            self.counter_break += 1
            self.in_hades_timer += 1
#RAPORT
            if self.timer > 1200:
                self.timer = 0
                if self.total_gold_expedition > 0 and self.total_xp_expedition > 0 and self.total_honour_expedition > 0:
                    print("Expeditions info:",self.total_gold_expedition, self.total_xp_expedition,self.total_honour_expedition, self.expedition_counter)
                if self.total_gold_arena > 0 and self.total_xp_arena > 0 and self.arena_counter > 0:
                    print("Arena info:",self.total_gold_arena, self.total_xp_arena, self.arena_win_counter, "/", self.arena_counter)
                if self.total_gold_circus > 0 and self.total_xp_circus > 0 and self.circus_counter > 0:
                    print("Circus info:",self.total_gold_circus, self.total_xp_circus, self.circus_win_counter, "/", self.circus_counter)
#BREAK & LEVEL COUNTER
            if self.counter_break > 59:
                self.counter_break = 0
                try:
                    view = driver.find_element(By.XPATH,'//*[@id="mainmenu"]/div[1]/a[1]')
                    driver.execute_script("$(arguments[0]).click();", view); time.sleep(3) 
                    expedition_current_points = driver.find_element(By.XPATH,'//*[@id="expeditionpoints_value_point"]').text
                    expedition_current_points = int(expedition_current_points)
                    expedition_max_points = driver.find_element(By.XPATH,'//*[@id="expeditionpoints_value_pointmax"]').text
                    expedition_max_points = int(expedition_max_points)
                    if expedition_max_points != 72 and expedition_max_points != 48 and expedition_current_points == 0 and break_time > 0 and self.in_hades == 0:
                        self.time_to_break = 1
                    else: self.time_to_break = 0
                except: time.sleep(0.001)
#BREAK
            if self.time_to_break == 1:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                if self.total_gold_expedition > 0 and self.total_xp_expedition > 0 and self.total_honour_expedition > 0:
                    print("Expeditions info:",self.total_gold_expedition, self.total_xp_expedition,self.total_honour_expedition, self.expedition_counter)
                if self.total_gold_arena > 0 and self.total_xp_arena > 0 and self.arena_counter > 0:
                    print("Arena info:",self.total_gold_arena, self.total_xp_arena, self.arena_win_counter, "/", self.arena_counter)
                if self.total_gold_circus > 0 and self.total_xp_circus > 0 and self.circus_counter > 0:
                    print("Circus info:",self.total_gold_circus, self.total_xp_circus, self.circus_win_counter, "/", self.circus_counter)
                print (current_time,"przerwa na", break_time, "sekund")
                self.time_to_break = 0
                time.sleep(break_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BotController()
    window.show()
    sys.exit(app.exec())