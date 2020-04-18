from django.db import models

# Create your models here.
class Customers(models.Model):
    firstname = models.CharField(max_length=30, blank=True, null=True)
    lastname = models.CharField(max_length=30, blank=True, null=True)
    nickname = models.CharField(max_length=20)
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
    name = models.CharField(max_length=30)
    #เท้าแชร์ยกหัวหนึ่งมือ
    admin_frist = models.BooleanField(default=True, help_text='เท้าแชร์ยกหัว')
    #เท้าแชร์หักท้ายหนึ่งมือ
    admin_last = models.BooleanField(default=True, help_text='เท้าแชร์หักค้ำท้าย')
    #รับตามมือจอง
    queue = models.BooleanField(default=True, help_text='รับตามมือจอง')
    #ฟิกเรต
    fix_rate = models.BooleanField(default=True, help_text='ฟิกเรต')
    #บิทแข่ง
    bit = models.BooleanField(default=True, help_text='บิท')
    #จำนวนมือ
    quantity = models.IntegerField(help_text='จำนวนมือ')
    #เงินต้น
    capital = models.IntegerField(help_text='เงินต้น', blank=True , null=True)
    #ส่งงวดละ
    payment = models.IntegerField(help_text='ส่งงวดละ', blank=True , null=True)
    #ดอกต่องวด
    interest = models.IntegerField(help_text='ดอกต่องวด', blank=True , null=True)
    #ส่งรายกี่วัน
    term = models.IntegerField(help_text='จำนวนวันที่ส่งต่องวด', blank=True , null=True)
    #วันเริ่มรันวง
    date_run = models.DateField(help_text='วันที่เริ่มวง')
    def __str__(self):
        return self.name

class Share_groups_customers(models.Model):
    #ชื่อกลุ่มแชร์
    share_group = models.ForeignKey(Share_groups, on_delete=models.CASCADE)
    #ลูกค้า
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE) 
    #วันที่ต้องส่งแชร์
    #รับแชร์มือที่
    receive_queue = models.IntegerField(help_text='ลำดับที่', blank=True , null=True)
    #ดอกเบี้ยต่องวด
    #วันที่รับแชร์
    class Meta:
        unique_together = ('share_group', 'receive_queue',)
    
    def __str__(self):
        text = self.customer.nickname
        text = text + ' ' + self.share_group.name
        text = text + ' ลำดับที่ ' + str(self.receive_queue)
        text = text + '/' + str(self.share_group.quantity)
        return text
        