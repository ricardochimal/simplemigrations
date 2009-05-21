from django.db import models

class AppliedMigration(models.Model):
	filename = models.TextField()
	version = models.IntegerField()

	def __unicode__(self):
		return self.filename

	@classmethod
	def latest(cls):
		ms = AppliedMigration.objects.all().order_by('-version')
		if len(ms):
			return ms[0] or None
		else:
			return None

	@classmethod
	def latest_version(cls):
		m = AppliedMigration.latest()
		if m:
			return m.version
		else:
			return 0
