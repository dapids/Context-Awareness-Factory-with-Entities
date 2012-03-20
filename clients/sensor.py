import sys, os, socket, re, time, random

head = '''\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::                Sensors simulator                :::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::
[ctrl+D to come back to the main menu] [ctrl+C to quit]'''

def pushData(data):
    print("Connecting to the server..")
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
        # Connect to server and send data
        sock.connect((sys.argv[1], int(sys.argv[2])))
        sock.sendall(data)
    
        # Receive data from the server and shut down
        sock.recv(1024)
    except Exception as e:
        print "Connection error:\n-> %s\n" % e
    else:
        print ("The server received '%s'.\n" % data)
    finally:
        sock.close()


def showMenu():
    cleanScr()
    print(head)
    print("\nChoose how to simulate a sensor:")
    print("\n\t1 -> Insert data by hand")
    print("\t2 -> Generate data randomly")
    print("\t3 -> Generate data randomly in debug mode\n")
    choice = raw_input()
    try:
        if int(choice) in range(1,4):
            if choice == "1":
                insertDataByHand()
            elif choice == "2":
                print("")
                generateData()
            else:
                print("")
                generateDataDebug()
        else:
            pass
    except ValueError:
        pass


def insertDataByHand():
    data = raw_input("\nInsert data in the following format: '[del] subject predicate object;'\n")
    flag = True
    while flag:
        if not data:
            data = raw_input("")
        else:
            flag = False
    print("")
    pushData(data.strip())
    raw_input("Press any key to come back to the main menu.")


def generateData():
    random.seed()
    while True:
        n = random.random()
        try:    
            inputFile = open(sys.argv[3], "r")
            for line in inputFile.readlines():
                pushData(line.strip())
                time.sleep(n*10)
        except IOError:
            print("Error while reading the file.")
            break
        except KeyboardInterrupt:
            break
        finally:
            inputFile.close()
        
        
def generateDataDebug():
    flag = True
    while flag:
        try:    
            inputFile = open(sys.argv[3], "r")
            for line in inputFile.readlines():
                try:
                    raw_input("Press any key to generate data..")
                except EOFError:
                    flag = False
                    break
                except KeyboardInterrupt:
                    flag = False
                    break
                else:
                    pushData(line.strip())
                finally:
                    inputFile.close()
        except IOError:
            print("Error while reading the file.")
            break
        except KeyboardInterrupt:
            break
        
        
def cleanScr():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("CLS")
        

if __name__ == '__main__':
    if len(sys.argv) == 4:
        if re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", sys.argv[1]):
            if re.match("^\d*$", sys.argv[2]):
                if os.path.isfile(sys.argv[3]):
                    while True:
                        try:
                            showMenu()
                        except KeyboardInterrupt:
                            sys.exit("\nGoodbye.")
                        except EOFError:
                            pass
                else:
                    print("Error. The file '%s' can not be found." % sys.argv[3])
            else:
                print("Please, insert a valid port:\n-> '%s' is not correct." % sys.argv[2])
        else:
            print("Please, insert a valid address:\n-> '%s' is not correct." % sys.argv[1])
    else:
        print("Please, launch me with this format:\n-> python2 %s serverAddress serverPort dataSourceFileName" % sys.argv[0])