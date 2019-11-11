from django.db import models
from django.db import IntegrityError
# Create your models here.

#To save auth refresh token.
class AuthToken(models.Model):
    token = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.token

class Shipment(models.Model):
    shipment_id = models.CharField(max_length=15, null=True, blank=True)
    shipment_ref = models.CharField(max_length=15, null=True, blank=True)
    shpiment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.shipment_id


'''
Try to use model manager if you face  integrityerror
while creating the object.
'''

#ShipmentItems Model Manager for adding multiple orders
class ShipmentItemManager(models.Model):
    def add_order(self, shipment=None, order_item_id=None, order_id=None):
        order = self.create(shipment=shipment,
                            order_item_id=order_item_id,
                            order_id=order_id)
        try:
            order.save()
        except IntegrityError:
        # Try again with other code
            return ShipmentItem.objects.add_order(shipment, order_item_id, order_id)
        else:
            return order

    def add_orders(self, shipment=None, order_item_id=None, order_id=None):
        orders = []
        orders.append(self.add_order(shipment, order_item_id, order_id)) 
        return orders                           

#Multiple order items can be  added to shipment
class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, null=True, blank=True, 
                                    on_delete=models.CASCADE, 
                                    related_name='shipment')
    order_item_id = models.CharField(max_length=15, null=True, blank=True)
    order_id =  models.CharField(max_length=15, null=True, blank=True)

    objects = ShipmentItemManager()



    class Meta:
        verbose_name = ("Order Item")
        verbose_name_plural = ("Order Items")


#Transport Model Manager for adding one transport to an shipment
class TransportManager(models.Model):
    def add_transport(self, shipment=None, transport_id=None):
        transport = self.create(shipment=shipment,
                            transport_id=transport_id,)
        try:
            transport.save()
        except IntegrityError:
        # Try again with other code
            return Transport.objects.add_transport(shipment, transport_id)
        else:
            return transport


# One transport can be assign to particular shipment
class Transport(models.Model):
    shipment = models.OneToOneField(Shipment, null=True, blank=True, 
                                    on_delete=models.CASCADE, related_name='transport')
    transport_id =  models.CharField(max_length=15, null=True, blank=True)                                    

    objects = TransportManager()

