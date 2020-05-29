from django.db import models
import time

# Create your models here.
class Customers(models.Model):
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)
    BANK_NAME = [
        ('BBL', 'ธนาคารกรุงเทพ'),
        ('BBC', 'ธนาคารกรุงเทพพาณิชย์การ'),
        ('KTB', 'ธนาคารกรุงไทย'),
        ('BAY', 'ธนาคารกรุงศรีอยุธยา'),
        ('KBANK', 'ธนาคารกสิกรไทย'),
        ('CITI', 'ธนาคารซิตี้แบงค์'),
        ('TMB', 'ธนาคารทหารไทย'),
        ('SCB', 'ธนาคารไทยพาณิชย์'),
        ('NBANK', 'ธนาคารธนชาติ'),
        ('SICB', 'ธนาคารนครหลวงไทย'),
        ('GSB', 'ธนาคารออมสิน'),
        ('GHB', 'ธนาคารอาคารสงเคราะห์'),
        ('BAAC', 'ธ.ก.ส.')
    ]
    bank_name = models.CharField(max_length=5, choices=BANK_NAME, blank=True, null=True)
    line = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return self.nickname

class Share_groups(models.Model):
    name = models.CharField(max_length=200)
    #เท้าแชร์ยกหัวหนึ่งมือ
    admin_frist = models.BooleanField(default=True, help_text='เท้าแชร์ยกหัว')
    #เท้าแชร์หักค้ำท้ายหนึ่งมือ
    admin_last = models.BooleanField(default=False, help_text='เท้าแชร์หักค้ำท้าย')
    #หักต้นวันรับ , วันรับไม่ต้องส่งยอด
    date_receive_no_payment = models.BooleanField(default=True, help_text='หักวันรับ')
    #รับตามมือจอง
    queue = models.BooleanField(default=False, help_text='รับตามมือจอง')
    #ฟิกเรต
    fix_rate = models.BooleanField(default=False, help_text='ฟิกเรต')
    #บิทแข่ง
    bit = models.BooleanField(default=False, help_text='บิท')
    #จำนวนมือ
    quantity = models.IntegerField(help_text='จำนวนมือ')
    #เงินต้น
    capital = models.IntegerField(help_text='เงินต้น', blank=True , null=True)
    #ส่งงวดละ
    payment = models.IntegerField(help_text='ส่งงวดละ', default=0)
    #ดอกต่องวด
    interest = models.IntegerField(help_text='ดอกต่องวด', default=0)
    #ส่งรายกี่วัน
    term = models.IntegerField(help_text='จำนวนวันที่ส่งต่องวด', blank=True , null=True)
    #วันที่ส่งต้องลงท้ายตรงกัน
    fix_last_date = models.BooleanField(default=False, help_text='วันที่ส่งต้องลงท้ายตรงกัน แชร์ราย10วันและ15วันต้องติ๊กตรงนี้ด้วย')
    #วันเริ่มรันวง
    date_run = models.DateField(help_text='วันที่เริ่มวง')
    #ปิดวง ไม่ต้องการให้แสดงผลแชร์วงนี้
    share_close = models.BooleanField(default=False, help_text='ปิดวง ไม่ต้องการให้แสดงผลแชร์วงนี้')
    #สร้างวันสร้างวันจ่ายแชร์
    build_share_pay_date = models.BooleanField(default=True, help_text='แสดงปุมสร้างวันจ่ายแชร์')
    def __str__(self):
        return self.name

class Share_groups_customers(models.Model):
    #ชื่อกลุ่มแชร์
    share_group = models.ForeignKey(Share_groups, on_delete=models.CASCADE, null=True)
    #ลูกค้า
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)    
    #รับแชร์มือที่    
    receive_queue = models.IntegerField(help_text='ลำดับที่ ต้องใส่ทุกครั้ง',default=1)
    #ฟิกเรต
    fix_rate = models.IntegerField(help_text='ฟิกเรต ใส่เฉพาะวงแชร์แบบฟิกเรต', default=0)
    #วันที่รับแชร์แบบบิท
    receive_date = models.DateField(help_text='วันที่เปียแชร์ ไม่ต้องใส่ โปรแกรมจะกำหนดให้อัตโนมัติ', blank=True, null=True)
    #ดอกเบี้ยที่บิท
    interest_bit = models.IntegerField(help_text='ดอกเบี้ยที่บิท ไม่ต้องใส่ โปรแกรมจะกำหนดให้อัตโนมัติ',default=0)
    class Meta:
        unique_together = ('share_group', 'receive_queue',)
    
    def __str__(self):
        text = self.customer.nickname
        text = text + ' , ' + self.share_group.name
        text = text + ' , ลำดับที่ ' + str(self.receive_queue)
        text = text + '/' + str(self.share_group.quantity)
        text = text + ' , ' + str(self.fix_rate)
        return text
        
class Share_pay_date(models.Model):
    share_groups_customers = models.ForeignKey(Share_groups_customers, on_delete=models.CASCADE, null=True)
    pay_date = models.DateField(help_text='วันที่ต้องส่ง', null=True)
    class Meta:
        unique_together = ('share_groups_customers', 'pay_date',)
    

#ลบข้อมูลทั้งหมดในtable = table.objects.all().delete()
'''
from share.models import Customers, Share_groups, Share_groups_customers, Share_pay_date
Share_pay_date.objects.all().delete()
'''
#delete migration=https://trameltonis.com/en/blog/how-reset-django-migrations/