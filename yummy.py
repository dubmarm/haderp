#!python
#http://www.plugged.in/linux/using-the-python-api-for-yum.html
#http://mo.morsi.org/blog/node/220
#http://stackoverflow.com/questions/8439074/determine-if-package-installed-with-yum-python-api
#http://yum.baseurl.org/wiki/YumCodeSnippets
#http://www.programcreek.com/python/example/59376/yum.YumBase

# import yum
# yb = yum.YumBase()
# print yb.conf.logfile # this will obviously printout the logfile's path
# for i in yb.conf.reposdir : print i # and this will printout the directories and files for the repositories
# print yb.conf.skip_broken # usually false. when set to true, your yum commands will take action of is the --skip-broken parameters was given to the yum itself.
# print yb.conf.errorlevel # this is the level of errors you'd like to get as an output. it's between 0-10 and 0 is only critical ones, 
# while 10 is more like a debug feature. Usually it is set to default 2, but since you'll be running in a script, after your script gets stable,
# its a good idea to set this to 0 and then distribute it.
# print yb.conf.config_file_path # obvious again, the file path for your yum's config file.

import yum
import os
import sys
import output
from urlgrabber.progress import TextMeter

yb=yum.YumBase()
yb.conf.cache = os.geteuid() != 0

# Use the "internal" output mode of yum's cli
sys.path.insert(0, '/usr/share/yum-cli')

yb.repos.setProgressBar(TextMeter(fo=sys.stdout))
yb.repos.callback = output.CacheProgressCallback()
yumout = output.YumOutput()
freport = ( yumout.failureReport, (), {} )
yb.repos.setFailureCallback( freport )


installed = [x.name for x in yb.rpmdb.returnPackages()]

class yummyintummy(object):
	def __init__(self, arg):
		self.arg = arg
		
	def yuminstall(self):
		for package in self.arg :
			if package in installed:
				print('{0} is already installed, skipping...'.format(package))
			else:
				print('Installing {0}'.format(package))
				kwarg = {
					'name':package
				}
				yb.install(**kwarg)
				yb.resolveDeps()
				yb.buildTransaction()
		yb.processTransaction()

	def yumremove(self):
		for package in self.arg :
			if package in installed:
				print('{0} is already installed, skipping...'.format(package))
			else:
				print('Installing {0}'.format(package))
				kwarg = {
					'name':package
				}
				yb.delete(**kwarg)
				yb.resolveDeps()
				yb.buildTransaction()
		yb.processTransaction()
		
# TEST
#arg=['pigz', 'tree']
#yummyintummy(arg).yuminstall()