# Generated by Django 3.2 on 2021-04-10 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankTeller',
            fields=[
                ('bank_teller_id', models.AutoField(primary_key=True, serialize=False)),
                ('account', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=11)),
                ('id_number', models.CharField(max_length=30)),
                ('deposit', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('fund_id', models.AutoField(primary_key=True, serialize=False)),
                ('fund_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LoanRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField()),
                ('payment', models.IntegerField()),
                ('repay_cycle', models.IntegerField()),
                ('left_payment', models.IntegerField()),
                ('left_fine', models.IntegerField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='RegularDeposit',
            fields=[
                ('regular_deposit_id', models.AutoField(primary_key=True, serialize=False)),
                ('regular_deposit_name', models.CharField(max_length=10)),
                ('return_cycle', models.IntegerField()),
                ('return_rate', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stock_id', models.AutoField(primary_key=True, serialize=False)),
                ('stock_name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='StockPriceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField()),
                ('price', models.FloatField()),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.stock')),
            ],
        ),
        migrations.CreateModel(
            name='StockInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_share', models.IntegerField()),
                ('cumulative_purchase_amount', models.FloatField()),
                ('purchase_date', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.customer')),
                ('stock_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.stock')),
            ],
        ),
        migrations.CreateModel(
            name='RegularDepositInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_amount', models.FloatField()),
                ('purchase_date', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.customer')),
                ('regular_deposit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.regulardeposit')),
            ],
        ),
        migrations.CreateModel(
            name='LoanRepay',
            fields=[
                ('repay_id', models.AutoField(primary_key=True, serialize=False)),
                ('left_payment_before', models.IntegerField()),
                ('left_fine_before', models.IntegerField()),
                ('repay', models.IntegerField()),
                ('repay_time', models.DateTimeField()),
                ('record_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.loanrecord')),
            ],
        ),
        migrations.CreateModel(
            name='FundPriceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateTimeField()),
                ('price', models.FloatField()),
                ('fund_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.fund')),
            ],
        ),
        migrations.CreateModel(
            name='FundInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_share', models.FloatField()),
                ('cumulative_purchase_amount', models.FloatField()),
                ('purchase_date', models.DateTimeField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.customer')),
                ('fund_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.fund')),
            ],
        ),
        migrations.CreateModel(
            name='DepositRecord',
            fields=[
                ('record_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField()),
                ('payment', models.IntegerField()),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bts.customer')),
            ],
        ),
    ]
