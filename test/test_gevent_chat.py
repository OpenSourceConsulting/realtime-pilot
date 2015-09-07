# -*- coding: utf-8 -*-

# 
# gevent 를 테스트하기 위한 코드
# echo() 또는 chat() 를 불러서 에코서버나 챗서버를 띄울수있다.
# 여러가지로 테스트 해보고 괜찮으면 사용을 해보자.
#
# 일단 컨셉은 session 을 상속받아서 소켓처리를 해주는 코드만 짜주면 되도록 하는것
# 좀더 신경써줄부분은
#
# 1. server.run 에서 그냥 start 를 부르게 해서 블러킹 막고 여러 서버를 동시에 돌릴수 있게 수정
# 2. session.mother.sessions 를 통해 다른 세션에 접근하는 방식이 적절한지 생각해볼것.
# 

import gevent
import gevent.server
import gevent.socket


def LOG(fmt, *args):
    print(str(fmt) % args)

class InvalidSessionNameError(StandardError):
    pass
class DuplicatedSessionNameError(StandardError):
    pass
class UnknownSessionNameError(StandardError):
    pass

class server:
    """연결을 받아서 적당한 세션을 까고 그 세션들을 기억해두는
    놈. 상속받아 쓰지 않고 기능을 추가해 나가는 식으로 만들었다.    
    """
    
    def __init__(self, session_class, addr=("0.0.0.0",9413), max_session = 10):
        self.session_class  = session_class
        self.listen_address = addr
        self.max_session    = max_session
        self.server         = gevent.server.StreamServer(addr, self.handle)
        self.sessions       = {}

    def run(self):
        LOG("listen at %s",self.listen_address)
        self.server.serve_forever()

    def handle(self, sock, addr):
        LOG("new connection from %s", addr)
        # 더이상 세션을 받을수 있는지 확인해보자
        if len(self.sessions) >= self.max_session:
            sock.close()
        c = self.session_class(self, sock, addr)
        c.run()

    # 
    # 이하는 세션목록을 관리하는 함수들, 아마 점점 커질텐데 어느정도
    # 커지면 session_manager 등으로 뽑아내는것도 고려해보자
    # 
    def add_session(self, si):  # si means session instance
        # 해당 세션이름이 이미 있다면 뭔가 잘못된것
        sname = si.session_name
        if sname in self.sessions:
            raise DuplicatedSessionNameError(sname)
        # 세션목록에 추가
        self.sessions[sname] = si
        LOG("add_session %s [%d/%d]", sname, len(self.sessions), self.max_session)
        return True

    def remove_sesion(self, si):
        sname = si.session_name
        if sname in self.sessions:
            del self.sessions[sname]
            LOG("remove_session %s [%d/%d]", sname, len(self.sessions), self.max_session)
        else:
            raise UnknownSessionNameError(sname)

class session:
    """실제 소켓을 물고 읽고 쓰고 할 놈.
    run 을 상속받아 구현하되 아래 순서를 신경쓸것
    1. 세션의 고유이름을 결정할것, 예를들어 ID 를 받는다던지 등등 이는 세션목록의 키값으로 쓰이니 주의깊게 결정.
    2. 이 고유이름을 session_name 필드에 채울것. 이후는 이 값을 손대지 않는다.
    3. session_name 이 채워진 후에는 register 를 부를것
    4. 필요한 작업
    5. 모든 작업이 끝나면 소켓을 닫고
    6. unregister 를 부를것.
    """
    def __init__(self, mother, sock, peer):
        self.mother = mother
        self.sock = sock
        self.name = None
        
    def run(self):
        pass

    def register(self):
        if not self.session_name:
            raise InvalidSessionNameError()
        return self.mother.add_session(self)
    def unregister(self):
        if not self.session_name:
            raise InvalidSessionNameError()
        self.mother.remove_sesion(self)

def echo():
    # 실제 사용할때는 session 을 적당히 상속받고 
    class echo(session):
        def run(self):
            self.session_name = str(self.sock)
            self.register()
            self.loop()
            self.unregister()
        def loop(self):
            while True:
                buf = self.sock.recv(1024)
                if buf:
                    self.sock.send(buf)
                else:
                    LOG("disconnected %s", self.session_name)
                    return
    # 서버에 이 클래스를 넘긴후 run 부르면 된다
    s = server(echo)
    s.run()

def chat():
    # 세션간에 서로 참조를 하는 예제
    # 클라가 처음 연결 물었을때 ID 를 물어보고 그 ID 를 세션키 삼아서 세션을 관리하도록 했다.
    # 현재는 별기능 없고 전체챗만 가능
    class chat(session):
        def run(self):
            userid = self.login()
            self.session_name = userid
            self.register()
            self.loop()
            self.unregister()
        def login(self):
            self.sock.send("type your name\r\n")            
            userid = self.readline_dirty()
            self.sock.send("hello %s\r\n" % userid)
            return userid
        def loop(self):
            self.hello_everybody()
            try:
                while True:
                    msg = self.readline_dirty()
                    self.with_all_sessions(lambda k,v: v.sock.send("%s says: %s\r\n" % (self.session_name, msg)))
            except:
                # 이건 완전 땜질. 소켓이 끊어지면 급조된
                # readline_dirty 가 예외질을 해서 적절히
                # 막아줬다. 서비스코드라면 에러대책을 세워야겠지.
                pass
            self.goodbye_everybody()

        def hello_everybody(self):
            self.with_all_sessions(lambda k,v: v.sock.send("*** %s joined\r\n" % self.session_name))

        def goodbye_everybody(self):
            self.with_all_sessions(lambda k,v: v.sock.send("*** %s left\r\n" % self.session_name))

        def with_all_sessions(self, fun):
            # 사실상 server 쪽에 위치해야 하는 함수인데 일단 예제니까.
            # 그냥 for 쓰는게 더 보기 좋지만 self.mother.sessions 로 접근하는게 후에 바뀔수 있으니 함수 하나로 모아뒀다.
            for k,v in self.mother.sessions.iteritems():
                fun(k,v)

        def readline_dirty(self):
            # makefile 을 통해서 readline 을 쓰는게 가능한데 예제코드라 그냥 이짓을 했다
            buf = ""
            while True:
                tmp = self.sock.recv(1)
                if tmp:
                    if tmp == "\n":
                        return buf.strip()
                    else:
                        buf += tmp
                else:
                    raise StandardError("readline error")
            
    s = server(chat)
    s.run()
            
if __name__ == "__main__":
    #echo()
    chat()