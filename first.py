import socket
import ssl 
from PIL import Image
import pickle as p

class URL:
    def __init__(self, url) -> None:
        if url[:12] == "view-source:":
            url = url[12:]
        self.url = url
        self.scheme, url = url.split("://",1)
        assert self.scheme in ["http", "https", "file"]
        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        if ":" in self.host:
            self.host, port = self.host.split(":",1)
            self.port = int(port)

    def request(self):
        #Olha, se alguém quiser contribuir, só falta msm adicionar sistema de caching de páginas, compressão e KeepAlive. Tmj abraço.
        if self.scheme == "file":
         #   im = Image.open(self.path)
          #  im.show()
          pass
        else:

            s = socket.socket(
                family= socket.AF_INET,
                type=socket.SOCK_STREAM,
                proto=socket.IPPROTO_TCP,
            )  
            s.connect((self.host, self.port))
            if self.scheme == "https":
                ctx = ssl.create_default_context()
                s = ctx.wrap_socket(s, server_hostname= self.host)
            request = "GET {} HTTP/1.0\r\n".format(self.path)
            request += "Host: {}\r\n".format(self.host)
            request += "User-Agent: Wacky PC\r\n"
            request += "\r\n"
            s.send(request.encode("utf8"))

            response = s.makefile("r", encoding="utf8", newline="\r\n")
            statusline = response.readline()
            version, status, explanation = statusline.split(" ", 2)
            response_headers = {}
            while True:
                line = response.readline()
                if line == "\r\n": break
                header, value = line.split(":",1)
                response_headers[header.casefold()] = value.strip()
            assert "transfer-encoding" not in response_headers
            
            if 'content-length' in response_headers:
                content = response.read(int(response_headers['content-length']))
            else:
                content = response.read()
            KeepAlive.keepSocket(KeepAlive(self.url, s))
            if(response_headers.__contains__('location') and status.startswith('3')):
                load(response_headers['location'])
            else:
                return content
    
def redirects(errorCode, locationHeader):
    i = 0
    pass
                
    
class KeepAlive(object):
    def __init__(self, url, socket) -> None:
        self.url = url
        self.socket = socket
    def keepSocket(self):
        dupla = KeepAlive(self.url, self.socket)
        with open('broserHistory.pkl', 'wb') as outp:
            p.dump("dupla.socket", outp, p.HIGHEST_PROTOCOL)
            #A linha acima não funciona, infelizmente pickle n consegue salvar websockets, 
            #Coloquei o que temos aqui dentro de um str() para não dar erro, mas o método
            #por enquanto é bem inútil. Se tiver alguém que saiba como salvar essas coisas forte abraço.
            




def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif c == "&lt;":
            c = "<"
        elif c == "&gt;":
            c = ">"
        elif not in_tag:
            print(c, end="")

def verify(url):
    mostused = {"wiki":"https://pt.wikipedia.org/wiki"}
    try:
        return mostused[url]
    except KeyError:
        return url

def load(url):
    url = verify(url)
    urlURL = URL(url)
    body = urlURL.request()
    if body != None and url[:12] != "view-source:":
        show(body)
    elif url[:12] == "view-source:":
        for c in body:
            print(c, end="")

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        show("escreve de novo burro")
    else:
        load(sys.argv[1])
