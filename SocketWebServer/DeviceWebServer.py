import socket
from _thread import *
import SocketWebServer.HTTPDefine as HTTPDefine 
import select

class DeviceWebServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.handler = {}
        self.commandName = ['method', 'url', 'version']
        self.threadRun = False
        
    def addHandler(self,key,value):
        self.handler[key] = value
                
    def runServer(self):
        self.threadRun = True
        print('--- DeviceWebServer Start.')
        print('--- Stop Server Command <Ctrl-C>')
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen()
        
        sockList = [self.serverSocket]
        while self.threadRun:
            try:
                r,w,e = select.select(sockList,[],[], 1)

                for r1 in r:
                    if(r1 == self.serverSocket):
                        clientSocket, addr = self.serverSocket.accept()
                        start_new_thread(self.response, (clientSocket, addr))
                    else:
                        pass
            except KeyboardInterrupt:
                print('--- Server Stop.')  
                self.stopServer()
        
    def stopServer(self):
        self.threadRun = False
        try:
            self.serverSocket.shutdown(socket.SHUT_RDWR)
            self.serverSocket.close()
        except :
            pass
            
    
    def headerParsing(self, headerData):        
        index = 0
        nameIndex = 0

        headerDic = {}

        for endline in headerData.split('\r\n'):
            print(endline)
            if index == 0:
                for cmdStr in endline.split(' '):
                    headerDic[self.commandName[nameIndex]] = cmdStr.strip()
                    nameIndex += 1
            else:
                keyValue = endline.split(':')
                headerDic[keyValue[0].strip()] = keyValue[1].strip()

            index += 1
        return headerDic
    
    def headerGen(self, statusCode, headers, bodyData):
        responseHeader = HTTPDefine.HEADER_VERSION11 + ' ' + HTTPDefine.statusCode[statusCode] + '\r\n'
        for key, val in headers.items():
            responseHeader += key + ': ' + val + '\r\n'
            
        responseHeader += '\r\n'
        print('\r\nResponse\r\n%s' %responseHeader)
        
        responseData = responseHeader.encode()
        
        if bodyData :
            responseData += bodyData
        return responseData
    
    def response(self, client_socket, addr):
        print('Connected by : ', addr[0], ':', addr[1])
        
        try:
            BUFSIZE = 4096

            isHeader = False

            headerDic = {}

            recvHeader = b''
            recvBody = b''

            totalRecvLen = -1
            totalLen = 0

            loopCount = 0

            while (totalRecvLen < totalLen) :
                packet = client_socket.recv(BUFSIZE)
                recvLen = len(packet)
                totalRecvLen += recvLen

                if not isHeader:
                    index = packet.decode(HTTPDefine.UTF8, 'ignore').find('\r\n\r\n')

                    if not index == -1:
                        recvHeader += packet[0: index]
                        recvBody += packet[index + 4: len(packet)]
                        isHeader = True
                        headerDic = self.headerParsing(recvHeader.decode(HTTPDefine.UTF8))

                        if HTTPDefine.HEADER_CONTENT_LENGTH in headerDic:
                            totalLen = int(headerDic[HTTPDefine.HEADER_CONTENT_LENGTH])
                            totalRecvLen = len(recvBody)

                        print('end header')
                    else:
                        recvHeader += packet
                else:
                    recvBody += packet
                loopCount += 1

            print('loopCount = %d' %loopCount)

        except Exception as e:
            print(e)
        
        resHeaders = {}
        resBody = None
        headerCode = "200"
        
        if headerDic[self.commandName[1]] in self.handler :            
            headerCode = "200"
            resBody = self.handler[headerDic[self.commandName[1]]](recvBody)
            resHeaders[HTTPDefine.HEADER_CONTENT_TYPE] = HTTPDefine.CONTENT_TYPE_OCTETSTREAM
            resHeaders[HTTPDefine.HEADER_CONTENT_LENGTH] = '%d' %len(resBody)
            resHeaders[HTTPDefine.HEADER_CONNECTION] = HTTPDefine.CONNECTION_CLOSE
        else:
            headerCode = "400"
            resHeaders[HTTPDefine.HEADER_CONNECTION] = HTTPDefine.CONNECTION_CLOSE

        client_socket.send(self.headerGen(headerCode, resHeaders, resBody))
        client_socket.close()