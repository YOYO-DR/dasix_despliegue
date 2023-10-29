from django.db.models.functions import Cast
from datetime import datetime
import calendar

from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.db.models import FloatField
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.inventario.models import Venta, Producto, DetalleVenta

from random import randint

meses_espanol = {
        1: 'enero',
        2: 'febrero',
        3: 'marzo',
        4: 'abril',
        5: 'mayo',
        6: 'junio',
        7: 'julio',
        8: 'agosto',
        9: 'septiembre',
        10: 'octubre',
        11: 'noviembre',
        12: 'diciembre',
    }

class DashboardView(TemplateView):
    template_name= 'dashboard.html'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_grafico_venta_mes':
                data = {
                    'name': 'Precio de venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.get_grafico_venta_mes()
                }
            elif action == 'get_grafico_producto_venta_mes':
                valoresG=self.get_grafico_producto_venta_mes()
                data = {"chart":{
                    'name': 'Porcentaje',
                    'colorByPoint': True,
                    'data': valoresG[0],
                },
                "mes":meses_espanol[valoresG[1]],
                "anio":valoresG[2]

                    
                }
            elif action == 'get_grafico_online':
                data = {'y': randint(1, 100)}
                print(data)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data={}
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_grafico_venta_mes(self):
        data=[]
        try:
            year=datetime.now().year
            for m in range(1,13):
                Total=Venta.objects.filter(Date_joined__year=year, Date_joined__month=m).aggregate(Total=Cast(Coalesce(Sum('Total'), 0.00),FloatField()))
                data.append(Total['Total'])
        except Exception as e:
            print(str(e))
        return data
    
    def get_grafico_producto_venta_mes(self):
        data = []
        year = datetime.now().year
        mes = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = DetalleVenta.objects.filter(Venta__Date_joined__year=year, Venta__Date_joined__month=mes, Produ_id=p.id).aggregate(r=Cast(Coalesce(Sum('Subtotal'), 0.00),FloatField())).get("r",0)
                if total > 0:
                    data.append({
                        'name': p.Nombre,
                        'y': float(total)
                    })
        except Exception as e:
            print(e)
        return [data, mes, year]


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['panel']='Panel de administrador'
        context['grafico_venta_mes']=self.get_grafico_venta_mes()
        context['ventas']=Venta.objects.all().order_by("-Date_joined")[0:10]
        produ=Producto.objects.filter(Stock__lt=6)
        context['alert_produ']={"vali":True if produ.exists() else False,"produ": produ }
        return context