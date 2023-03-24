# Generated by Django 3.2.15 on 2023-03-24 13:44
from django.contrib.auth import get_user_model
from django.db import migrations, models


User = get_user_model()


class Migration(migrations.Migration):

    dependencies = [
        ('misago_users', '0023_remove_user_sso_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_fields',
            field=models.JSONField(),
        ),
        migrations.RunSQL(
            sql=migrations.RunSQL.noop,
            reverse_sql='''
            create or replace function pg_temp.jsonb2hstore(jdata jsonb)
            returns hstore
            as $$
                select COALESCE(hstore(array_agg(key), array_agg(value)), hstore(''))
                from jsonb_each_text(jdata)
            $$ language sql immutable strict;
            ALTER TABLE {} ALTER COLUMN profile_fields TYPE hstore USING pg_temp.jsonb2hstore(profile_fields);
            '''.format(User._meta.db_table),
            elidable=True,
        )
    ]
