from __future__ import with_statement

from django.conf import settings

import os
import re

slug_regex = re.compile('[^a-z0-9_]')
migration_file_regex = re.compile('(\d+)_([a-z0-9_]+)\.py')

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
			if os.path.isfile(os.path.join(settings.MIGRATION_DIRECTORY, f))]

	def migration_files(self):
		return [f for f in self.files() if migration_file_regex.match(f)]

	def max_migration(self):
		nums = [int(migration_file_regex.match(f).groups()[0]) for f in self.migration_files()]
		if len(nums):
			return max(nums)
		else:
			return 0

