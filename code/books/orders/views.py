from django.shortcuts import render

def list_orders(request):
    
    return render(request, 'orders/purchase.html', {'title':'Orders'})
