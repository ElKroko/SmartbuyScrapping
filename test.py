import csv
from difflib import *
from math import prod
from pickletools import TAKEN_FROM_ARGUMENT1


def csv_to_list(filename, list):
    with open(filename, 'r') as file:    
        csvr = csv.reader(file)
        for producto in csvr:
            list.append(producto)      # Del csv a una lista

def csv_tottus(filename, list):
    with open(filename, 'r') as file:
        csvr = csv.reader(file)
        with open("lista_productos.csv", "w") as file2:
            for producto in csvr:
                list.append(producto)
                link = producto[1]
                file2.write(link + "\n")    # Creo un archivo para todos los links de los productos del tottus
                                        # Para buscar sus EAN en cada pagina particularmente.

# Buscar la posicion del header que necesitamos en el csv, retorna -1 si no encuentra.

def position(header, lista):
    pos = -1
    for i in range(len(lista)):
        if header == lista[i]: pos = i
    return pos




# Probar con get_close_matches 

def nombres_similares(nombre1, nombre2):
    nom1 = nombre1.strip().casefold()
    nom2 = nombre2.strip().casefold()

    print()
    print("nombres similares")

    print("Nom1: ",nom1)
    print("Nom2: ",nom2)

    seq1 = SequenceMatcher(nom1, nom2)
    seq2 = SequenceMatcher(nom2, nom1)

    # print(seq1.ratio())
    # print(seq2.ratio())
    
    lista_nom1 = nom1.split(" ")
    lista_nom2 = nom2.split(" ")

    # Caso Arroces: G1 en vez de grado 1

    if "g1" in nom1:
        # print("Cambiar nombre! G1")
        
        lista_temp = list()
        for palabra in lista_nom1:
            if palabra == "g1":
                lista_temp.append("grado 1")
            else:
                lista_temp.append(palabra)
        nom1 = " ".join(lista_temp)
        lista_nom1 = nom1.split(" ")
        print(nom1)

    # Caso Arroces: G2 en vez de grado 2
    if "g2" in nom1:
        # print("Cambiar nombre! G2")
        lista_temp = list()
        for palabra in lista_nom1:
            if palabra == "g2":
                lista_temp.append("grado 2")
            else:
                lista_temp.append(palabra)
        nom1 = " ".join(lista_temp)
        lista_nom1 = nom1.split(" ")    
        print(nom1)


    # Idea para hacer match: revisar palabra por palabra si es que una de nom1 seencuentra dentro de nom2, y agregar
    # un contador para sacar un porcentaje de palabras contenidas.
    # Caso sensible: que nom 1 tenga muy pocas palabras, pero que todas esten dentro de nom2.
        # Podria arreglar este caso sensible si es que saco cant y unit del nombre del jumbo?

    cont_1 = 0
    tot_1 = len(lista_nom1)
    cont_2 = 0
    tot_2 = len(lista_nom2)


    for palabra_1 in lista_nom1:
        if palabra_1 in lista_nom2: cont_1 += 1
    for palabra_2 in lista_nom2: 
        if palabra_2 in lista_nom1: cont_2 += 1

    per_1 = cont_1 / tot_1
    per_2 = cont_2 / tot_2
    print (per_1, "\t", per_2)

    if per_1 == 1:
        if per_2 > 0.2:
            print ("YESSSSSS")
            print("nom1 in nom2")
            return True
    elif per_2 == 1:
        if per_1 > 0.2:
            print ("YESSSSSS")
            print("nom2 in nom1")
            return True
        
    # elif seq1.ratio() < 0.8:                     #   
    #     d = Differ()
    #     diff = d.compare([nom1], [nom2])
    #     print("La diferencia es: \n", "\n".join(diff))
    #     print("Sin match...")
    #     return False
    else:
        return False




#
#   Retorna si el producto es exclusivo o no, y en el caso de no ser exclusivo, el SKU y precio del producto en encontrado en la tienda
#


#
# Extrae la cantidad y unidad de un producto a partir del titulo, siguiendo el formato del Jumbo.
#   Ademas, entrega el nombre sin estas cantidades asociadas, eliminandolas del string.

def extraer_unit_cant(titulo):
    unidades = ["kg", "g", "cc", "ml", "l", "lt"]

    palabras = titulo.split(" ")

    cant = 0
    unit = ""

    pos_cant = 0
    pos_unit = 0

    for i in range(len(palabras)):
        if palabras[i].isnumeric():
            if i+1 <= len(palabras):
                unidad = palabras[i+1].replace(",","")
                if unidad in unidades:
                    cant = palabras[i]
                    pos_cant = i
                    pos_unit = i+1
                    unit = unidad
    
    del palabras[pos_cant]
    del palabras[pos_unit-1]
    
    nombre = " ".join(palabras)

    return nombre, cant, unit


# funcion que retorna la informacion necesaria para adjuntar al producto, o False, "" y 0.
def buscar_producto_jumbo(producto, jumbo):
    nom = producto["title"]
    print("El nombre en tottus es: ", nom)
    marca = producto["brand"].lower()
    cantidad = producto["cant"]
    unit = producto["unit"].lower()
    print("Marca: ", marca)
    print("cantidad: ", cantidad)
    print("unit: ", unit)


    for prod_jumbo in jumbo[1:]:
        brand_j = prod_jumbo[2].lower()
        titulo = prod_jumbo[0]
        

        title_j, cant_j, unit_j = extraer_unit_cant(titulo)
        
        if cant_j == cantidad and unit_j == unit:
            if brand_j == marca:
                print()
                print("Pseudo Match! para:\t", titulo)
                if nombres_similares(nom, title_j):
                    print()
                    print("Match confirmed")
                    link_j = prod_jumbo[1]
                    SKU_j = prod_jumbo[-1][8:]
                    precio_j = "".join(prod_jumbo[4].strip("$").split("."))


                    return True, link_j, SKU_j, precio_j
    
    return False, "", 0, 0

def ini_producto(ean, title, cant, unit, brand, prod_link, img_link):
    producto = dict()
    producto["ean"] = ean
    producto["title"] = title
    producto["cant"] = cant
    producto["unit"] = unit
    producto["brand"] = brand
    producto["exclusive"] = 0
    producto["description"] = ""
    producto["slug"] = ""
    producto["img_link"] = img_link
    producto["category_id"] = ""
    
    #SKU
    producto["sku_lider"] = 0
    producto["sku_jumbo"] = 0
    
    # Precios
    producto["price_j"] = 0
    producto["price_l"] = 0
    producto["price_t"] = 0
    # Links (para futuras busquedas del producto)
    producto["link_tottus"] = prod_link
    producto["link_jumbo"] = ""
    producto["link_lider"] = ""

    return producto

# GLOBALES
categorias = ["Arroz", "Papas Fritas", "Cervezas"]

if __name__ == "__main__":
    lider = []
    jumbo = []
    tottus = []
    ean_tottus = []

    csv_to_list("Jumbo.csv", jumbo)
    csv_to_list("Lider.csv", lider)
    csv_tottus("Tottus.csv", tottus)
    csv_to_list("EAN_productos.csv", ean_tottus)

    

    # print(lider)


    lista_productos = []
    



    for i in range(len(ean_tottus)):
        if (i == 0): continue   #skip header
        title = ean_tottus[i][0]
        html_ean = ean_tottus[i][1]
        marca_cant_unit = ean_tottus[i][2].split("-")

        brand = marca_cant_unit[0].strip()
        cant = marca_cant_unit[1].strip().split(" ")[0]
        unit = marca_cant_unit[1].strip().split(" ")[1]

        ean_list = html_ean.split(" ")
        ean = ean_list[2][10:-1]        # data-ean="XXXXX"
        
        # print(title + "\t" + ean + "\t" + brand +"\t" + cant + "\t" + unit)

        prod_link = tottus[i][1]
        img_link = tottus[i][2]

        pre_price = tottus[i][4][1:-2].split(".")
        pre_cmr_price = tottus[i][5][1:-2].split(".")

        price = "".join(pre_price).strip()
        cmr_price = "".join(pre_cmr_price).strip()

        # print(price, cmr_price)
        
        producto = ini_producto(ean, title, cant, unit, brand, prod_link, img_link)

        
        cond, link_j, SKU_j, precio_j = buscar_producto_jumbo(producto, jumbo)
        if cond:
            producto["link_jumbo"] = link_j
            producto["sku_jumbo"] = SKU_j
        lista_productos.append(producto)

    print()
    print("Resultados:")
    print (cond, link_j, SKU_j)

    # print(nombres_similares("An", "Joabn"))

    #




    # CSV fields
    #
    # ean           ok
    # title         ok
    # exclusive     Si es que lo encuentro una vez, no lo es.
    # description   PUEDO SACARLO DEL JUMBO?
    # slug          
    # pack          
    # cant          ok
    # unit          ok
    # image         
    # brand         ok
    # url_img_ext   IMG link del Tottus.
    # category_id

    # Otros fields utiles:
    # Link_lider
    # Link_jumbo
    # Link_Tottus
    # Precio_j
    # Precio_T
    # Precio_L
    # SKU_L
    # SKU_J




    #Comentarios para el futuro:

    '''
    Tengo que programar como discernir si es exclusive o no
    Tengo que ver como obtener si es Pack o no
    definir como obtener el "unit"
    Como funcionan las categorias?
        - Hasta ahora manual

    UPD: 11/02/22

    - En el jumbo, los arroces estan categorizados en 2:
        - Arroz
        - Arroz Preparado y Especial

    - Por esto, debo unir los scrapping de ambas categorias en un csv antes de buscar un producto del tottus.

    Futuras updates:
    - Debo revisar nombres_similares, para que realmente entregue una similitud correcta...
        - Que pasa cuando por ejemplo, un nombre es: arroz integral
        y el otro es arroz integral multigrano 400 gr?

'''
    
'''Idea: podria hacer que los productos en los supermercados fueran diccionarios, para acceder mas facil a ellos?

Cual es el criterio para buscar un producto y hacer match?
- Mismo nombre      ... cuanta similitud?
- Misma presentacion (Cant, unit)
- misma marca

producto: deberia ser un diccionario.

'''

'''
14/02

Tengo que revisar que productos son encontrados y cuales no, escribiendo la lista_productos en un csv
tengo que devolver el valor exclusive = 0 cuando encuentre los productos en el jumbo
- lo mismo para el lider




'''


 
