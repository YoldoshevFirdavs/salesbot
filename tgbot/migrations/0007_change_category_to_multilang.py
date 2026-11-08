# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0006_remove_product_description_product_description_eng_and_more'),
    ]

    operations = [
        # Add new fields with null=True temporarily
        migrations.AddField(
            model_name='category',
            name='name_eng',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_uz',
            field=models.CharField(max_length=255, null=True),
        ),
        # Copy data from old name field to new fields
        migrations.RunPython(
            code=lambda apps, schema_editor: [
                setattr(cat, 'name_uz', cat.name) or 
                setattr(cat, 'name_ru', cat.name) or 
                setattr(cat, 'name_eng', cat.name) or 
                cat.save()
                for cat in apps.get_model('tgbot', 'Category').objects.all()
            ],
            reverse_code=migrations.RunPython.noop,
        ),
        # Make fields non-nullable
        migrations.AlterField(
            model_name='category',
            name='name_eng',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uz',
            field=models.CharField(max_length=255),
        ),
        # Remove old name field
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        # Update ordering
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name_uz'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]
