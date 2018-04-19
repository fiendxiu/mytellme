# Generated by Django 2.0 on 2018-01-10 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tellme', '0003_noc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fastline',
            name='level',
        ),
        migrations.AddField(
            model_name='fastline',
            name='bkpe',
            field=models.CharField(blank=True, max_length=50, verbose_name='备PE'),
        ),
        migrations.AddField(
            model_name='fastline',
            name='bkport',
            field=models.CharField(blank=True, max_length=20, verbose_name='备接口'),
        ),
        migrations.AddField(
            model_name='fastline',
            name='bkwanip',
            field=models.CharField(blank=True, max_length=20, verbose_name='备WANIP'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='apppass',
            field=models.CharField(blank=True, max_length=120, verbose_name='APP账号密码'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='contractname',
            field=models.CharField(max_length=255, verbose_name='合同名'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='mrtg',
            field=models.CharField(blank=True, max_length=120, verbose_name='MRTG链接'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='mrtgpass',
            field=models.CharField(blank=True, max_length=80, verbose_name='MRTG账号密码'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='netflow',
            field=models.CharField(blank=True, max_length=120, verbose_name='Netflow链接'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='netflowpass',
            field=models.CharField(blank=True, max_length=80, verbose_name='Netflow账号密码'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='sales',
            field=models.EmailField(max_length=254, verbose_name='业务邮箱'),
        ),
        migrations.AlterField(
            model_name='cid',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='fastline',
            name='bandwidth',
            field=models.CharField(max_length=50, verbose_name='带宽'),
        ),
        migrations.AlterField(
            model_name='fastline',
            name='fastport',
            field=models.CharField(blank=True, max_length=20, verbose_name='接口'),
        ),
        migrations.AlterField(
            model_name='fastline',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='flanline',
            name='bandwidth',
            field=models.CharField(max_length=50, verbose_name='带宽'),
        ),
        migrations.AlterField(
            model_name='flanline',
            name='flanid',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='组网ID'),
        ),
        migrations.AlterField(
            model_name='flanline',
            name='flanport',
            field=models.CharField(blank=True, max_length=20, verbose_name='接口'),
        ),
        migrations.AlterField(
            model_name='flanline',
            name='level',
            field=models.CharField(choices=[('MAIN', 'MAIN'), ('BACKUP', 'BACKUP')], default='MAIN', max_length=10, verbose_name='主/备'),
        ),
        migrations.AlterField(
            model_name='flanline',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='jituan',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='localline',
            name='bandwidth',
            field=models.CharField(max_length=50, verbose_name='带宽'),
        ),
        migrations.AlterField(
            model_name='localline',
            name='localid',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='厂商ID'),
        ),
        migrations.AlterField(
            model_name='localline',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='monitorline',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='siline',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='状态'),
        ),
        migrations.AlterField(
            model_name='site',
            name='siteaddr',
            field=models.CharField(blank=True, max_length=255, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='site',
            name='status',
            field=models.CharField(choices=[('ON', 'ON'), ('OFF', 'OFF'), ('ON_TEST', 'ON_TEST')], default='ON_TEST', max_length=8, verbose_name='站点状态'),
        ),
    ]
