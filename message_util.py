import socket

import message
from message import Message
from message_header import Header
from message_body import BodyRequest
from message_body import BodyResponse
from message_body import BodyData
from message_body import BodyResult

class MessageUtil:
    @staticmethod
    def send(sock, msg):
        sent = 0
        buffer = msg.GetBytes()
        while sent < msg.GetSize():
            sent += sock.send(buffer)
    @staticmethod
    def receive(sock):
        print('3')
        totalRecv = 0
        sizeToRead = 16
        hBuffer = bytes()
        print('4')
        
        while sizeToRead > 0:
            print("암튼",sizeToRead)
            buffer = sock.recv(sizeToRead)
            print('버그1')
            if not buffer:
                return None
            print('버그2')
            
            hBuffer += buffer
            print('버그3')
            totalRecv += len(buffer)
            print('버그4')
            sizeToRead -= len(buffer)
            print("암튼",hBuffer)
            print("암튼",totalRecv)
        
        print('5')
        
        header = Header(hBuffer)
        print('6')
        
        totalRecv = 0
        bBuffer = bytes()
        sizeToRead = header.BODYLEN
        
        while sizeToRead > 0:
            buffer = sock.recv(sizeToRead)
            if not buffer:
                return None
                
            bBuffer += buffer
            totalRecv += len(buffer)
            sizeToRead -= len(buffer)
        
        body = None
        
        if header.MSGTYPE == message.REQ_FILE_SEND:
            body = BodyRequest(bBuffer)
        elif header.MSGTYPE == message.REP_FILE_SEND:
            body = BodyResponse(bBuffer)
        elif header.MSGTYPE == message.FILE_SEND_DATA:
            body = BodyData(bBuffer)
        elif header.MSGTYPE == message.FILE_SEND_RES:
            body = BodyResult(bBuffer)
        else:
            raise Exception(
                "Unknown MSGTYPE : {0}".format(header.MSGTYPE))
        
        msg = Message()
        
        msg.Header = header
        msg.Body = body
        
        return msg