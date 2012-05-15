import socket, sys, re, os
import pickle

head = '''\n:::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::                Information retriever            :::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::
[ctrl+D to delete your query] [ctrl+C to quit]'''

def sendData(data):
    print("Connecting to the server..")
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    try:
        # Connect to server and send data
        sock.connect((sys.argv[1], int(sys.argv[2])))
        sock.sendall(data)
    
        # Receive data from the server and shut down
        received = sock.recv(1024)
        received = pickle.loads(received)
    except Exception as e:
        print "Connection error:\n-> %s\n" % e
    else:
        print ("Answer from from the server:")
        for row in received:
            if isinstance(row, tuple):
                sys.stdout.write("->\t")
                for i, el in enumerate(row):
                    if el is not None:
                        if i < len(row)-1:
                            sys.stdout.write("%s " % el)
                        else:
                            sys.stdout.write("%s\n" % el)
            else:
                if row is not None:
                    print("->\t%s" % row)
    finally:
        sock.close()

    
def askQuery():
    cleanScr()
    print(head)
    query = raw_input("\nPlease, insert your SPARQL query and be sure that it ends with '!!':\n\n")
    flag = True
    while flag:
        if "!!" in query:
            flag = False
        else:
            query = query + " " + raw_input().strip()
    print("")
    sendData(query)
    raw_input("\nPress any key to formulate a new query.\n")
    
    
def cleanScr():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("CLS")
    
    
if __name__ == '__main__':
    if len(sys.argv) == 3:
        if re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", sys.argv[1]):
            if re.match("^\d*$", sys.argv[2]):
                while True:
                    try:
                        askQuery()
                    except KeyboardInterrupt:
                        sys.exit("\nGoodbye.")
                    except EOFError:
                        pass
            else:
                print("Please, insert a valid port:\n-> '%s' is not correct." % sys.argv[2])
        else:
            print("Please, insert a valid address:\n-> '%s' is not correct." % sys.argv[1])
    else:
        print("Please, launch me with this format:\n-> python2 %s serverAddress serverPort" % sys.argv[0])