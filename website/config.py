import configparser

def loadConfig(filepath)
config_object= configparser.ConfigParser()
#read config file into object
config_object.read(filepath)
for sect in config_object.sections():
   print('Section:', sect)
   for k,v in config_object.items(sect):
      print(' {} = {}'.format(k,v))
   print()