#import re
#import os
#import sys
from django.core.management.base import BaseCommand, CommandError
#from django.core.management.color import no_style
#from optparse import make_option
from django.conf import settings
#from django.db import models

#import pprint

class Command(BaseCommand):
	help = "Generate a new migration"
	requires_model_validation = True

	actions = ['create', 'apply']

	def handle(self, *args, **options):
		if args:
			print "some stuff"
		else:
			print "Use this tool to generate migrations"
			for command in self.__class__.actions:
				method = getattr(self, command)
				print " ./manage.py migration %s %s" % (command, method.__doc__)

# 		available_args = db_generator.get_commands()
# 		if args:
# 			arg, remaining = args[0], args[1:]
# 			if arg in available_args:
# 				available_args[arg](remaining, options.get('output'))
# 			else:
# 				# Print help and exit
# 				raise CommandError('Available options are %s' % ', '.join(
# 					available_args.keys())
# 				)
# 		else:
# 			# Print instructions
# 			print "Use this tool to generate migrations"
# 			for arg, fn in available_args.items():
# 				print "  ./manage.py migration %s%s" % (arg, fn.__doc__)
# 			print "  Use the --output option to view a migration without " \
# 				"writing it to disk"

	def create(self, *args, **kwargs):
		"""Create new migration"""
		pass

	def apply(self, *args, **kwargs):
		"""Apply migrations"""
		pass

