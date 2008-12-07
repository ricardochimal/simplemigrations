


class UndefinedMigration(Exception):
	pass

class InvalidMigration(Exception):
	pass


class BaseMigration(object):
	def __init__(self):
		self._sql = []

	def up(self):
		raise UndefinedMigration, 'up method is undefined'

	def down(self):
		raise UndefinedMigration, 'down method is undefined'

	def add_column(self, **kwargs):
		Column(self, **kwargs).add()

	def drop_column(self, **kwargs):
		Column(self, **kwargs).drop()

	def rename_column(self, **kwargs):
		Column(self, **kwargs).rename()

	def execute(self, sql):
		self._sql.append(sql)
		self._cursor.execute(sql)

	@property
	def _cursor(self):
		# TODO: database cursor ?.
		pass


class Column(object):
	def __init__(self, migration, app, model, column, field_type=None, rename_to_column=None):
		self.migration = migration
		self.app = app
		self.model = model
		self.column = column
		self.rename_to_column = rename_to_column
		self.field_type = field_type

	@property
	def table(self):
		return u"%s_%s" % (self.app, self.model)

	def add(self):
		if not self.field:
			raise InvalidMigration, 'Adding %s requires field_type' % self.column

		sql = 'ALTER TABLE %(table)s ADD COLUMN %(column)s %(field_type)s' % {
			'table' : self.table,
			'column' : self.column,
			'field_type' : self.field_type,
		}
		self.migration.execute(sql)

	def drop(self):
		sql = 'ALTER TABLE %(table)s DROP COLUMN %(column)s' % {
			'table' : self.table,
			'column' : self.column,
		}
		self.migration.execute(sql)

	def rename(self):
		if not self.rename_to_column:
			raise InvalidMigration, 'Renaming %s requires rename_to_column' % self.column

		sql = 'ALTER TABLE %(table)s RENAME COLUMN %(column)s TO %(rename_to_column)s' % {
			'table' : self.table,
			'column' : self.column,
			'rename_to_column' : self.rename_to_column,
		}
		self.migration.execute(sql)


