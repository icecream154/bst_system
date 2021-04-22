# Generated by Django 3.2 on 2021-04-11 10:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bts', '0005_auto_20210411_1655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='bank_teller_id',
            new_name='bank_teller',
        ),
        migrations.RenameField(
            model_name='depositrecord',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='fundinvestment',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='fundinvestment',
            old_name='fund_id',
            new_name='fund',
        ),
        migrations.RenameField(
            model_name='fundpricerecord',
            old_name='fund_id',
            new_name='fund',
        ),
        migrations.RenameField(
            model_name='loanrecord',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='loanrepay',
            old_name='loan_record_id',
            new_name='loan_record',
        ),
        migrations.RenameField(
            model_name='regulardepositinvestment',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='regulardepositinvestment',
            old_name='regular_deposit_id',
            new_name='regular_deposit',
        ),
        migrations.RenameField(
            model_name='stockinvestment',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='stockinvestment',
            old_name='stock_id',
            new_name='stock',
        ),
        migrations.RenameField(
            model_name='stockpricerecord',
            old_name='stock_id',
            new_name='stock',
        ),
        migrations.AlterField(
            model_name='depositrecord',
            name='created_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='depositrecord',
            name='payment',
            field=models.FloatField(),
        ),
    ]
