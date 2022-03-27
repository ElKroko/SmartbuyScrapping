import csv
from difflib import *
from datetime import datetime
from math import prod
from turtle import title

path_lista_productos = "lista_productos.csv"


def csv_to_list(filename, list):
    with open(filename, 'r', encoding='UTF8') as file:    
        csvr = csv.reader(file)
        for producto in csvr:
            list.append(producto)      # Del csv a una lista

def csv_tottus(filename, list):
    with open(filename, 'r', encoding='UTF8') as file:
        csvr = csv.reader(file)
        with open(path_lista_productos, "w") as file2:
            for producto in csvr:
                list.append(producto)
                link = producto[1]
                file2.write(link + "\n")    # Creo un archivo para todos los links de los productos del tottus
                                        # Para buscar sus EAN en cada pagina particularmente.

def matches_logrados_jumbo(lista):
    c = 0
    for producto in lista:
        if producto["sku_jumbo"] != 0:
            c += 1
    return c, len(lista)

def matches_logrados_lider(lista):
    c = 0
    for producto in lista:
        if producto["sku_lider"] != 0:
            c += 1
    return c, len(lista)

def debug_log(lista_de_productos, opt):
    with open("logs/debug_log_jumbo.txt", opt) as file:

        now = datetime.now()
        file.write("JUMBO\n\n")
        curr = now.strftime("%H:%M")
        cant_matches , totales= matches_logrados_jumbo(lista_de_productos)
        file.write("Hora: "+curr)
        file.write("\n")
        file.write("Cantidad de Matches: " + str(cant_matches))
        file.write("\n")
        file.write("Cantidad de productos: "+ str(totales))
        file.write("\n")
        miss = 100 - (cant_matches/totales)*100
        file.write("Miss rate: " + str(miss) + "%")
        file.write("\n")
        file.write("\n")
        file.write("Matched Products (Tottus-Jumbo):\n")
        for elem in matched_products_jumbo:
            n_tottus, n_jumbo = elem
            s_t = "Tottus: " + n_tottus
            s_j = "Jumbo: " + n_jumbo
            file.write(s_t)            
            file.write("\n")
            file.write(s_j)
            file.write("\n")
            file.write("\n")

    with open("logs/debug_log_lider.txt", opt) as file:

        now = datetime.now()
        file.write("LIDER\n\n")
        curr = now.strftime("%H:%M")
        cant_matches , totales= matches_logrados_lider(lista_de_productos)
        file.write("Hora: "+curr)
        file.write("\n")
        file.write("Cantidad de Matches: " + str(cant_matches))
        file.write("\n")
        file.write("Cantidad de productos: "+ str(totales))
        file.write("\n")
        miss = 100 - (cant_matches/totales)*100
        file.write("Miss rate: " + str(miss) + "%")
        file.write("\n")
        file.write("\n")
        file.write("Matched Products (Tottus-Lider):\n")
        for elem in matched_products_lider:
            n_tottus, n_lider = elem
            s_t = "Tottus: " + n_tottus
            s_l = "Lider: " + n_lider
            file.write(s_t)            
            file.write("\n")
            file.write(s_l)
            file.write("\n")
            file.write("\n")


    

# Funcion que actualiza los csvs producidos por el programa    
def update_csvs(lista_de_productos):
    lista_csv = []
    csv_to_list('csv_to_bd/main_core_product.csv', lista_csv)
    lista_og = []
    for elem in lista_csv:
        if elem[0] == "ean": continue
        lista_og.append(elem[0])
    lista_nueva = []
    for elem in lista_de_productos:
        lista_nueva.append(elem['ean'])


    productos_por_agregar = list(set(lista_nueva)- set(lista_og) )
    
    print(lista_og)
    print(lista_nueva)
    print(productos_por_agregar)

    productos_nuevos = []
    cuantos_nuevos = 0
    for elem in lista_de_productos:
        for prod in productos_por_agregar:
            if elem["ean"] == prod:
                productos_nuevos.append(elem)
                cuantos_nuevos += 1
    
    print("De los ", len(lista_de_productos), " productos por agregar")
    print("Se encontro que ", len(productos_nuevos), " no estaban en la base de datos ")

    with open('csv_to_bd/main_core_product.csv', "a", encoding='UTF8', newline='') as main_products:
        writer = csv.writer(main_products)

        for product in productos_nuevos:
            data = [product['ean'], product['title'], product['exclusive'], product['description'], product['slug'], product['pack'], product['cant'], product['unit'], product['image'], product['brand'], product['img_link'], product['category_id']]
            writer.writerow(data)
            print("agregue producto", product)

    with open('csv_to_bd/main_core_skuprice.csv', 'a', encoding='UTF8', newline='') as file2:
        writer = csv.writer(file2)
        i = 1
        for product in productos_nuevos:
            #lider
            data = [i, product['sku_lider'], product['price_l'], id_supermercado['lider'], product['ean'] ]
            writer.writerow(data)
            i +=1
            
            # tottus:
            data = [i, product['sku_tottus'], product['price_t'], id_supermercado['tottus'], product['ean'] ]
            writer.writerow(data)
            i +=1
            # jumbo:
            data = [i, product['sku_jumbo'], product['price_j'], id_supermercado['jumbo'], product['ean'] ]
            writer.writerow(data)
            i +=1

    debug_log(lista_de_productos, opt="a")

# Funcion para construir los archivos CSV a usar en la BD
def list_to_csv(lista_de_productos):
    # Hoja productos:
    with open('csv_to_bd/main_core_product.csv', "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        header = ['ean', 'title','exclusive','description','slug', 'pack','cant', 'unit','image','brand','url_img_ext', 'category_id' ]
        writer.writerow(header)

        for product in lista_de_productos:
            data = [product['ean'], product['title'], product['exclusive'], product['description'], product['slug'], product['pack'], product['cant'], product['unit'], product['image'], product['brand'], product['img_link'], product['category_id']]
            writer.writerow(data)
    
    with open('csv_to_bd/main_core_skuprice.csv', 'w', encoding='UTF8', newline='') as file2:
        writer = csv.writer(file2)
        header = ['id', 'sku', 'price', 'branch_id', 'product_id']  # Branch_id es supermercado, product_id es ean
        writer.writerow(header)
        
        i = 1
        for product in lista_de_productos:
            #lider
            data = [i, product['sku_lider'], product['price_l'], id_supermercado['lider'], product['ean'] ]
            writer.writerow(data)
            i +=1
            
            # tottus:
            data = [i, product['sku_tottus'], product['price_t'], id_supermercado['tottus'], product['ean'] ]
            writer.writerow(data)
            i +=1
            # jumbo:
            data = [i, product['sku_jumbo'], product['price_j'], id_supermercado['jumbo'], product['ean'] ]
            writer.writerow(data)
            i +=1

    debug_log(lista_de_productos, opt="w")

# Buscar la posicion del header que necesitamos en el csv, retorna -1 si no encuentra.

def position(header, lista):
    pos = -1
    for i in range(len(lista)):
        if header == lista[i]: pos = i
    return pos




# Probar con get_close_matches 

def nombres_similares(nombre1, nombre2, marca, superm):
    nom1 = nombre1.strip().casefold()
    nom2 = nombre2.strip().casefold()

    print(superm)
    print()

    # print("Nom1: ",nom1)
    # print("Nom2: ",nom2)

    lista_nom1 = nom1.split(" ")
    lista_nom2 = nom2.split(" ")

    # Caso Arroces: G1 en vez de grado 1

    if "g1" in nom1:      
        lista_temp = list()
        for palabra in lista_nom1:
            if palabra == "g1":
                lista_temp.append("grado 1")
            else:
                lista_temp.append(palabra)
        nom1 = " ".join(lista_temp)
        lista_nom1 = nom1.split(" ")
        # print("Cambio de nombre a: ", nom1)

    # Caso Arroces: G2 en vez de grado 2
    if "g2" in nom1:
        lista_temp = list()
        for palabra in lista_nom1:
            if palabra == "g2":
                lista_temp.append("grado 2")
            else:
                lista_temp.append(palabra)
        nom1 = " ".join(lista_temp)
        lista_nom1 = nom1.split(" ")    
        # print("Cambio de nombre a: ",nom1)

    cont_1 = 0
    tot_1 = len(lista_nom1)
    cont_2 = 0
    tot_2 = len(lista_nom2)

    if marca in lista_nom1:
        # print(marca, 'removed from l1')
        lista_nom1.remove(marca)
    if marca in lista_nom2:
        lista_nom2.remove(marca)
        # print(marca, 'removed from l2')

    for palabra_1 in lista_nom1:
        for palabra_2 in lista_nom2:
            if palabra_1 == '1' and palabra_2 == '2':
                    break
            if palabra_1 == palabra_2:
                    cont_1 += 1
        # if palabra_1 in lista_nom2: cont_1 += 1
    for palabra_2 in lista_nom2: 
        for palabra_1 in lista_nom2:
            if palabra_2 == '1' and palabra_1 == '2':
                    break
            if palabra_1 == palabra_2:
                    cont_2 += 1
        # if palabra_2 in lista_nom1: cont_2 += 1

    per_1 = cont_1 / tot_1
    per_2 = cont_2 / tot_2
    print (per_1, "\t", per_2)

    threshold = 3/5

    if per_1 >threshold:
        if per_2 > threshold:
            print("nom1 in nom2")
            return True
    elif per_2 > threshold:
        if per_1 > threshold:
            print("nom2 in nom1")
            return True
    else:
        return False


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
    
    # print (titulo)

    if len(palabras)>1:
        del palabras[pos_cant]
        del palabras[pos_unit-1]
    
    nombre = " ".join(palabras)

    return nombre, cant, unit

def buscar_producto_lider(producto, lider):
    nom = producto["title"].lower()
    marca = producto["brand"].lower()
    cantidad = producto["cant"].lower()
    unit = producto["unit"].lower()

    for prod_lider in lider[1:]:
        title_l = prod_lider[0].lower()
        brand_l = prod_lider[2].lower()
        uni_cant = prod_lider[6].split(" ")
        if len(uni_cant)>1:
            cant_l = uni_cant[0]
            unit_l = uni_cant[1]
        else:
            unit_l = 1
            cant_l = uni_cant[0]

        
        if cant_l == cantidad and unit_l == unit:
            if brand_l == marca:
                if nombres_similares(nom, title_l, marca, superm="lider"): 

                    SKU_l = prod_lider[1].strip("()Ref: ")
                    price_l = "".join(prod_lider[5].strip("$").split("."))
                    link_l = prod_lider[3]

                    matched_products_lider.append((nom, title_l))
                    return True, link_l, SKU_l, price_l
    
    return False, "", 0, 0
        




# funcion que retorna la informacion necesaria para adjuntar al producto, o False, "" y 0.
def buscar_producto_jumbo(producto, jumbo):
    nom = producto["title"].lower()
    marca = producto["brand"].lower()
    cantidad = producto["cant"].lower()
    print(nom)
    unit = producto["unit"].lower()

    for prod_jumbo in jumbo[1:]:
        brand_j = prod_jumbo[1].lower()
        titulo = prod_jumbo[0].lower()
        

        title_j, cant_j, unit_j = extraer_unit_cant(titulo)
        link_j = prod_jumbo[2]

        if cant_j == cantidad and unit_j == unit:   
            if brand_j == marca:
                # print("link_jumbo", link_j)
                
                if nombres_similares(nom, title_j, marca, superm="lider"):      # Revisamos si nombres hacen match
                    print()
                    print("Match confirmed")
                    SKU_j = prod_jumbo[7][9:]
                    precio_verde = "".join(prod_jumbo[4].strip("$").split("."))
                    precio_gris = "".join(prod_jumbo[5].strip("$").split("."))
                    precio_rojo = "".join(prod_jumbo[6].strip("$").split("."))
                    
                    if precio_verde == "": precio_verde = 999999
                    if precio_gris == "": precio_gris = 999999
                    if precio_rojo == "": precio_rojo = 999999

                    precio_j = min(int(precio_verde),int(precio_rojo),int(precio_gris))

                    descr = prod_jumbo[8]
                    
                    matched_products_jumbo.append((nom, title_j))

                    return True, link_j, SKU_j, precio_j, descr
                print()
    if producto["sku_jumbo"] == 0:
        print("No hay match para: ", nom, " marca: ", marca)

    return False, "", 0, 0, ''


# Funcion para inicializar un producto, el cual es un diccionario.
def ini_producto(ean, title, cant, unit, brand, prod_link, img_link, cmr_price):
    producto = dict()
    producto["ean"] = ean
    producto["title"] = title
    producto["cant"] = cant
    producto["unit"] = unit
    producto["brand"] = brand
    producto["exclusive"] = 1
    producto["description"] = ""
    producto["slug"] = ""
    producto['image'] = ''
    producto["img_link"] = img_link
    producto["category_id"] = which_category(title)
    producto['pack'] = ''
    
    #SKU
    producto["sku_lider"] = 0
    producto["sku_jumbo"] = 0
    producto['sku_tottus'] = 0
    
    # Precios
    producto["price_j"] = 0
    producto["price_l"] = 0
    producto["price_t"] = cmr_price
    # Links (para futuras busquedas del producto)
    producto["link_tottus"] = prod_link
    producto["link_jumbo"] = ""
    producto["link_lider"] = ""

    return producto

# Funcion para construir lista de productos ingresando la lista del tottus.

def del_tottus(tottus):
    lista_productos = []

    for i in range(len(tottus)):
        if (i == 0): continue   #skip header
        title = tottus[i][0]
        prod_link = tottus[i][1]
        img_link = tottus[i][2]
        
        marca_cant_unit = tottus[i][3].split(" - ")
        # print(marca_cant_unit)
        brand = marca_cant_unit[0].strip()
        uni_cant = marca_cant_unit[1].strip().split(" ")
        if len(uni_cant)>1:
            cant = uni_cant[0]
            unit = uni_cant[1]
        else:
            unit = "1"
            cant = uni_cant[0]

        html_ean = tottus[i][4]
        ean_list = html_ean.split(" ")
        ean = ean_list[2][10:-1]        # data-ean="XXXXX"

        pre_cmr_price = tottus[i][5][1:-2].split(".")
        cmr_price = "".join(pre_cmr_price).strip()


        producto = ini_producto(ean, title, cant, unit, brand, prod_link, img_link, cmr_price)

        lista_productos.append(producto)
    return lista_productos


def is_exclusive(producto):
    if producto["sku_jumbo"] != 0 or producto["sku_lider"] != 0:
        return False
    else:
        return True

def which_category(title):
    category = 0

    if "arroz" in title.casefold():
        category = categorias["arroz"]
    if "cerveza" in title.casefold():
        category = categorias["cervezas"]
    if "papa frita" in title.casefold():
        category = categorias["snack"]


    return category

#   =============================================================
#                   Main Program
#   =============================================================

# GLOBALES
departamentos = {1: ["Aceites y Aderezos", "Snack", "Arroz"], 3:["Leche", "Yoghurt"], 6:["Cervezas"]}
departamentos_nombre = {1:"Despensa", 3:"Frescos y Lacteos", 6:"Bebidas y Licores"}

categorias = {"arroz":6, "snack":5, "cervezas":2}

id_supermercado = {'lider': 1, 'tottus' : 2, 'jumbo':3}

matched_products_jumbo = []
matched_products_lider = []

if __name__ == "__main__":
    lider = []
    jumbo = []
    tottus = []

    arroz_csv_jumbo = "To_scrap\Arroz-JumboData-ScrapeStorm.csv"
    arroz_csv_lider = 'To_scrap\Arroz-LiderData-ScrapeStorm.csv'
    arroz_csv_tottus = 'To_scrap\Arroz-TottusData-ScrapeStorm.csv'

    csv_to_list(arroz_csv_jumbo, jumbo)
    csv_to_list(arroz_csv_lider, lider)
    csv_to_list(arroz_csv_tottus, tottus)

    

    lista_productos = del_tottus(tottus)

    
    for producto in lista_productos:
        
        cond, link_j, SKU_j, precio_j, descr = buscar_producto_jumbo(producto, jumbo)
        if cond:
            producto["link_jumbo"] = link_j
            producto["sku_jumbo"] = SKU_j
            producto["price_j"] = precio_j
            producto["description"] = descr

        

        cond, link_l, SKU_l, price_l = buscar_producto_lider(producto, lider)
        if cond:
            print('Encontre lider')
            producto["link_lider"] = link_l
            producto["sku_lider"] = SKU_l
            producto["price_l"] = price_l
        
        producto["exclusive"] = is_exclusive(producto)


    list_to_csv(lista_productos)        # Para crear los CSV usados en la BD

    print("\t \t UPDATE CSV CERVEZAS AAAAA =============================================")

    matched_products_jumbo = []
    matched_products_lider = []

    # cervezas_csv_jumbo = "To_scrap\Cervezas-JumboData-ScrapeStorm.csv"
    # cervezas_csv_lider = 'To_scrap\Cervezas-LiderData-ScrapeStorm.csv'
    # cervezas_csv_tottus = 'To_scrap\Cervezas-TottusData-ScrapeStorm.csv'

    cervezas_csv_jumbo = "To_scrap\Papas Fritas-JumboData-ScrapeStorm.csv"
    cervezas_csv_lider = 'To_scrap\Papas Fritas-LiderData-ScrapeStorm.csv'
    cervezas_csv_tottus = 'To_scrap\Papas Fritas-TottusData-ScrapeStorm.csv'


    tottus_2 = []

    csv_to_list(cervezas_csv_jumbo, jumbo)
    csv_to_list(cervezas_csv_lider, lider)
    csv_to_list(cervezas_csv_tottus, tottus_2)

    

    lista_productos_2 = del_tottus(tottus_2)

    
    for producto in lista_productos_2:
        
        cond, link_j, SKU_j, precio_j, descr = buscar_producto_jumbo(producto, jumbo)
        if cond:
            producto["link_jumbo"] = link_j
            producto["sku_jumbo"] = SKU_j
            producto["price_j"] = precio_j
            producto["description"] = descr

        

        cond, link_l, SKU_l, price_l = buscar_producto_lider(producto, lider)
        if cond:
            print('Encontre lider')
            producto["link_lider"] = link_l
            producto["sku_lider"] = SKU_l
            producto["price_l"] = price_l
        
        producto["exclusive"] = is_exclusive(producto)

    

    update_csvs(lista_productos_2)        # Si existen, para actualizarlos




#Comentarios para el futuro:

'''
Tengo que ver como obtener si es Pack o no

15/02

Documentar como funciona un match entre productos

'''

    # Idea para hacer match: revisar palabra por palabra si es que una de nom1 seencuentra dentro de nom2, y agregar
    # un contador para sacar un porcentaje de palabras contenidas.
    # Caso sensible: que nom 1 tenga muy pocas palabras, pero que todas esten dentro de nom2.
    # Podria arreglar este caso sensible si es que saco cant y unit del nombre del jumbo?
 

'''
Nuevo caso sensible:
Hay algunos items en el tottus etiquetados como "INDIVIDUAL"
'''