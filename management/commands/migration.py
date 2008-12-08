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
			action = arg, remaining = args[0], arg[1:]
			if action not in self.__class__.actions
				raise CommandError('Available commands are %s' % ', '.join(self.__class__.actions)

			method =  getattr(self, action)
			method(remaining, options)
		else:
			print "Use this tool to generate migrations"
			for command in self.__class__.actions:
				method = getattr(self, command)
				print " ./manage.py migration %s %s" % (command, method.__doc__)

	def create(self, *args, **kwargs):
		"""[name] Create new migration"""
		from simplemigrations.templates import migration_template


	def apply(self, *args, **kwargs):
		"""Apply migrations"""
		pass

