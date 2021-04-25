from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import Developer

def developer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='developer')
		instance.groups.add(group)
		Developer.objects.create(
			user=instance,
			name=instance.username,
			)
		print('Profile created!')

post_save.connect(developer_profile, sender=User)