import datetime

def generate_order_umber(pk):
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S') #20260111181510 + pk
    order_number = current_datetime + str(pk)
    return order_number