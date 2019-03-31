from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nopassword', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logincode',
            name='user',
        ),
        migrations.DeleteModel(
            name='LoginCode',
        ),
    ]
