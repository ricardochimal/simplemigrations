from __future__ import with_statement

from django.db import transaction
from django.conf import settings

import os
import re

slug_regex = re.compile('[^a-z0-9_]')
migration_file_regex = re.compile('^(\d+)_([a-z0-9_]+)\.py$')

class Migration(object):
	def __init__(self):
		pass

	def create(self, name):
		from simplemigrations.template import migration_template

		new_filename = os.path.join(settings.MIGRATION_DIRECTORY, self.new_filename(name))

		with open(new_filename, "w") as f:
			f.write(migration_template)

		return new_filename

	def new_filename(self, name):
		slug_name = self.name_to_slug(name)
		num = self.max_migration() + 1
		return "%04d_%s.py" % (num, slug_name)

	def name_to_slug(self, name):
		name = name.lower().replace(' ', '_')
		return slug_regex.sub('', name)

	def files(self):
		return [f for f in os.listdir(settings.MIGRATION_DIRECTORY) \
			if os.path.isfile(os.path.join(settings.MIGRATION_DIRECTORY, f)) and migration_file_regex.match(f)]

	def migration_files(self):
		return [f for f in self.files() if migration_file_regex.match(f)]

	def migration_files_with_version(self):
		return [(f, int(migration_file_regex.match(f).groups()[0])) for f in self.migration_files()]

	def max_migration(self):
		nums = [t[1] for t in self.migration_files_with_version()]
		if len(nums):
			return max(nums)
		else:
			return 0

	def migrations_to_run(self):
		from simplemigrations.models import AppliedMigration
		latest_version = AppliedMigration.latest_version()
		return sorted([t for t in self.migration_files_with_version() if t[1] > latest_version], key=lambda x: x[1])

	def migration_file(self, version):
		for t in self.migration_files_with_version():
			if t[1] == version:
				return t[0]
		return None

	def load_migration_model(self, file_path):
		import imp
		dir_name, file_name = os.path.split(file_path)
		mod_name = file_name.replace('.py', '')
		dot_py_suffix = ('.py', 'U', 1)
		mod = imp.load_module(mod_name, open(file_path), file_path, dot_py_suffix)
		return mod

	@transaction.commit_manually
	def run(self):
		for t in  self.migrations_to_run():
			file_name, version = t
			file_path = os.path.join(settings.MIGRATION_DIRECTORY, file_name)
			klass = self.load_migration_model(file_path)
			self.migrate_up(klass, file_name, version)
			transaction.commit()

	@transaction.autocommit
	def migrate_up(self, klass, file_name, version):
		from simplemigrations.models import AppliedMigration

		m = klass.Migration()
		m.run(action='up')
		AppliedMigration.objects.create(filename=file_name, version=version)
		#transaction.commit_unless_managed()

	@transaction.autocommit
	def migrate_down(self, klass, instance):
		m = klass.Migration()
		m.run(action='down')
		instance.delete()
		#transaction.commit_unless_managed()

	@transaction.commit_manually
	def redo(self):
		from simplemigrations.models import AppliedMigration

		am = AppliedMigration.latest()
		version = am.version
		file_name = self.migration_file(version)
		file_path = os.path.join(settings.MIGRATION_DIRECTORY, file_name)
		klass = self.load_migration_model(file_path)

		self.migrate_down(klass, am)
		self.migrate_up(klass, file_name, version)

		transaction.commit()

