#-*- coding: UTF-8 -*- 
import socket  
import sys
import random
import json
import time

citys = []
sentence = None

def load_sentence():
    global sentence
    f = open("sentence.json")
    sentence = json.load(f)
    f.close()

def load_citys():
    global citys
    f = open("city.json")
    citys = json.load(f)
    f.close()

def get_random_element(array):
    return array[random.randint(0, len(array) - 1)];

def gen_random_nick():
    return "ustreamer-" + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9)) + str(random.randint(1, 9))

def gen_type():
    if random.choice([True, False]):
        subject_type = get_random_element(sentence["type"])
        if random.choice([True, False]):
            age = str(random.randint(1, 9)*10) + u"多年"
        else:
            age = ""
        return age + subject_type 
    else:
        return ""

def gen_location():
    city = citys[random.randint(0, len(citys) - 1)]
    city_name = city["name"]
    if random.choice([True, False]):
        city_name = city_name.replace(u"縣", "").replace(u"市", "")

    if random.choice([True, False]):
        region = get_random_element(city["regions"])
    else:
        region = ""

    return city_name + region

def gen_title():
    title = get_random_element(sentence["title"])
    if title != "":
        title_suffix = get_random_element(sentence["title_suffix"])
    else:
        title_suffix = ""
    return title + title_suffix

def gen_subject():
    location = gen_location()
    subject_type = gen_type()
    return location + subject_type

def gen_question():
    question = get_random_element(sentence["question"])
    question_suffix = get_random_element(sentence["question_suffix"])
    return question + question_suffix

def gen_message():
    title = gen_title()
    subject = gen_subject()
    question = gen_question()
    return title + subject + question

def main():

    if len(sys.argv) != 4:
        print("Usage: bot <server[:port]> <channel> <period>")
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
    period = float(sys.argv[3])

    load_citys()
    load_sentence()

    while 1:
        try:
            nick = gen_random_nick()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server, port))
            sock.send("NICK %s\r\n" % (nick))
            sock.send("USER %s 0 * :%s\r\n" % (nick, nick))
            sock.send("JOIN %s\r\n" % (channel))
            sock.send(("PRIVMSG %s :%s\r\n" % (channel, gen_message())).encode("utf-8"))
            sock.send("QUIT :%s\r\n" % ("Bye"))
            sock.close()
            time.sleep(period)
        except KeyboardInterrupt:
            print "exit!"
            exit(1)
        except:
            print "continue"

if __name__ == "__main__":
    main()