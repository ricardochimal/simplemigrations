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

	actions = ['create', 'run', 'redo', 'undo']

	def handle(self, *args, **options):
		if args:
			action, remaining = args[0], args[1:]
			if action not in self.__class__.actions:
				raise CommandError('Available commands are %s' % ', '.join(self.__class__.actions))

			method = getattr(self, action)
			method(*remaining, **options)
		else:
			print "Use this tool to generate migrations"
			for command in self.__class__.actions:
				method = getattr(self, command)
				print " ./manage.py migration %s %s" % (command, method.__doc__)

	def create(self, *args, **kwargs):
		"""[name] Create new migration"""

		from simplemigrations.actions import Migration
		new_file = Migration().create(args[0])
		print "Created new migration file: %s" % new_file

	def run(self, *args, **kwargs):
		"""Run migrations"""
		from simplemigrations.actions import Migration
		Migration().run()

	def redo(self, *args, **kwargs):
		"""Redo last migration"""
		from simplemigrations.actions import Migration
		Migration().redo()

	def undo(self, *args, **kwargs):
		"""Undo last migration"""
		from simplemigrations.actions import Migration
		Migration().undo()

