migration_template = """
from simplemigrations.migrations import BaseMigration, IrreversibleMigration

class Migration(BaseMigration):
	def up(self):
		# self.execute("SELECT 1")
		# self.add_column("myproject", "mymodel", "column", "integer")
		# self.drop_column("myproject", "mymodel", "column")
		# self.rename_column("myproject", "mymodel", "column", "renamed")
		pass

	def down(self):
		raise IrreversibleMigration, "down is not defined"
"""
