
 #!/usr/bin/python3
 #encoding: utf-8

# from subprocess import Popen, PIPE
# import re
#
# def getIfconfig():
#     p = Popen(['ifconfig'], stdout = PIPE)
#     data = p.stdout.read().split('\n\n')
#     return [i for i in data if i and not i.startswith('lo')]
#
# def parseIfconfig(data):
#     dic = {}
#     # re.M 多行模式，改变'^'和'$'的行为
#     for line in data:
#         re_devname = re.compile(r'(\w+).*Link encap', re.M)
#         re_macaddr = re.compile(r'HWaddr\s([0-9A-F:]{17})', re.M)
#         re_ipaddr  = re.compile(r'inet addr:([\d\.]{7,15})', re.M)
#         devname  = re_devname.search(line)
#         mac      = re_macaddr.search(line)
#         ip       = re_ipaddr.search(line)
#         if devname:
#              devname = devname.group(1)
#         else:
#              devname = ''
#
#         if mac:
#             mac = mac.group(1)
#         else:
#              mac = ''
#
#         if ip:
#              ip = ip.group(1)
#         else:
#              ip = ''
#         dic[devname] = [mac, ip]
#     return dic
#
# if __name__ == '__main__':
#      data = getIfconfig()
#      print (parseIfconfig(data))


from subprocess import Popen, PIPE

def getIP():
    p = Popen(['ifconfig'], stdout = PIPE, stderr = PIPE)
    stdout, stderr = p.communicate()
    data = [i for i in stdout.split('\n') if i]
    return data

def genIP(data):
    new_line = ''
    lines = []
    for line in data:
         if line[0].strip():
            lines.append(new_line)
            new_line = line + '\n'
         else:
            new_line += line + '\n'
    lines.append(new_line)
    return [i for i in lines if i and not i.startswith('lo')]

def parseIP(data):
    dic = {}
    for devs in data:
        lines = devs.split('\n')
        devname = lines[0].split()[0]
        macaddr = lines[0].split()[-1]
        ipaddr  = lines[1].split()[1].split(':')[1]
        dic[devname] = [ipaddr, macaddr]
        return dic

if __name__ == '__main__':
    data = getIP()
    nics = genIP(data)
    print (parseIP(nics))



from subprocess import Popen, PIPE

def getIfconfig():
   p = Popen(['ifconfig'], stdout = PIPE)
   data = p.stdout.read().split("\n\n")
   return [i for i in data if i and not i.startswith('lo')]

def parseIfconfig(data):
    dic = {}
    for devs in data:
        lines = devs.split('\n')
        devname = lines[0].split()[0]
        macaddr = lines[0].split()[-1]
        ipaddr  = lines[1].split()[1].split(':')[1]
        dic[devname] = [ipaddr, macaddr]
        return dic

if __name__ == '__main__':
    data = getIfconfig()
    print (parseIfconfig(data))