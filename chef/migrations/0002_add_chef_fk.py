from django.db import migrations


class Migration(migrations.Migration):
    """
    TiDB Cloud Serverless does not support adding a FK column via Django's
    standard AddField. We use raw SQL to add the columns without FK constraints.
    TiDB does not enforce FK constraints by default.
    """

    dependencies = [
        ('chef', '0001_initial'),
    ]

    operations = [
        # Add chef_id column to chef_fooditem
        migrations.RunSQL(
            sql="ALTER TABLE chef_fooditem ADD COLUMN chef_id bigint NOT NULL DEFAULT 1;",
            reverse_sql="ALTER TABLE chef_fooditem DROP COLUMN chef_id;",
        ),
        # Add chef_id column to chef_chefprofile
        migrations.RunSQL(
            sql="ALTER TABLE chef_chefprofile ADD COLUMN chef_id bigint NOT NULL DEFAULT 1;",
            reverse_sql="ALTER TABLE chef_chefprofile DROP COLUMN chef_id;",
        ),
        # Add unique constraint on chefprofile.chef_id (OneToOne)
        migrations.RunSQL(
            sql="ALTER TABLE chef_chefprofile ADD UNIQUE KEY chef_chefprofile_chef_id_unique (chef_id);",
            reverse_sql="ALTER TABLE chef_chefprofile DROP KEY chef_chefprofile_chef_id_unique;",
        ),
    ]
