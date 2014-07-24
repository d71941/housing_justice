#-*- coding: UTF-8 -*- 
import socket  
import sys
import random
import json

citys = []

def load_citys():
	global citys
	f = open("city.json")
	citys = json.load(f)
	f.close()

def gen_random_nick():
    return "ustreamer-" + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9))

def gen_random_message():
	city = citys[random.randint(0, len(citys) - 1)]
	region_name = city["regions"][random.randint(0, len(city["regions"]) - 1)]
	price = random.randint(10, 100)
	return u"%s%s%d萬可以買嗎？" % (city["name"], region_name, price)

def main():
	if len(sys.argv) != 3:
	    print("Usage: bot <server[:port]> <channel>")
	    sys.exit(1)

	s = sys.argv[1].split(":", 1)
	server = s[0]
	if len(s) == 2:
	    try:
	        port = int(s[1])
	    except ValueError:
	        print("Error: Erroneous port.")
	        sys.exit(1)
	else:
	    port = 6667
	channel = sys.argv[2]

	load_citys()

	while 1:
		nick = gen_random_nick()
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((server, port))
		sock.send("NICK %s\r\n" % (nick))
		sock.send("USER %s 0 * :%s\r\n" % (nick, nick))
		sock.send("JOIN %s\r\n" % (channel))
		sock.send(("PRIVMSG %s :%s\r\n" % (channel, gen_random_message())).encode("utf-8"))
		sock.send("QUIT :%s\r\n" % ("Bye"))
		sock.close()

if __name__ == "__main__":
    main()