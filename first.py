import socket
import ssl 
from PIL import Image

class URL:
    def __init__(self, url) -> None:
        self.scheme, url = url.split("://",1)
        assert self.scheme in ["http", "https"]
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
        if self.scheme == "file":
            im = Image.open(self.path)
            im.show()
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
            request += "close\r\n"
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
            content = response.read()
            s.close()
            return content
    
class data:
    def __init__(self, text):
        self.scheme, self.text = text.split(",", 2)
    def response(self):
        return self.text


def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")

def load(url):
    body = url.request()
    if body != None:
       show(body)

if __name__ == "__main__":
    import sys
    if len(sys.argv)<2:
        show("escreve de novo burro")
    else:  
        print(data.response(data(sys.argv[1])))
        #load(URL(sys.argv[1]))