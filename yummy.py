#!python
#http://www.plugged.in/linux/using-the-python-api-for-yum.html

# import yum
# yb = yum.YumBase()
# print yb.conf.logfile # this will obviously printout the logfile's path
# for i in yb.conf.reposdir : print i # and this will printout the directories and files for the repositories
# print yb.conf.skip_broken # usually false. when set to true, your yum commands will take action of is the --skip-broken parameters was given to the yum itself.
# print yb.conf.errorlevel # this is the level of errors you'd like to get as an output. it's between 0-10 and 0 is only critical ones, while 10 is more like a debug feature. Usually it is set to default 2, but since you'll be running in a script, after your script gets stable, its a good idea to set this to 0 and then distribute it.
# print yb.conf.config_file_path # obvious again, the file path for your yum's config file.

import yum


yb=yum.YumBase()
searchlist=['name']
arg=['pigz']
matches = yb.searchGenerator(searchlist,arg)
for (package, matched_value) in matches :
    if package.name == 'pigz' : yb.install(package)
    yb.buildTransaction()
    yb.processTransaction()