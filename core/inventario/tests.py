from config.wsgi import *
from core.inventario.models import *


data = ["Leche y derivados", "Carnes, pescados y huevos", "Patatas, legumbres, frutos secos",
        "Verduras y Hortalizas", "Frutas", "Cereales y derivados, azúcar y dulces",
        "Grasas, aceite y mantequilla"]
for valor in data:

    Categoria(Nombre=valor).save()
    

# delete from public.erp_Categoria;
# ALTER SEQUENCE erp_category_id_seq RESTART WITH 1;

#letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           #'u', 'v', 'w', 'x', 'y', 'z']

#for i in range(1, 6000):
    #name = ''.join(random.choices(letters, k=5))
   # while Categoria.objects.filter(Nombre=name).exists():
        #name = ''.join(random.choices(letters, k=5))
    #Categoria(Nombre=name).save()
    #print('Guardado registro {}'.format(i))
