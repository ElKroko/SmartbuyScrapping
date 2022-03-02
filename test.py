import csv
from difflib import *
from datetime import datetime

path_lista_productos = "lista_productos.csv"


def csv_to_list(filename, list):
    with open(filename, 'r') as file:    
        csvr = csv.reader(file)
        for producto in csvr:
            list.append(producto)      # Del csv a una lista

def csv_tottus(filename, list):
    with open(filename, 'r') as file:
        csvr = csv.reader(file)
        with open(path_lista_productos, "w") as file2:
            for producto in csvr:
                list.append(producto)
                link = producto[1]
                file2.write(link + "\n")    # Creo un archivo para todos los links de los productos del tottus
                                        # Para buscar sus EAN en cada pagina particularmente.

def matches_logrados(lista):
    c = 0
    for producto in lista:
        if producto["sku_lider"] != 0 or producto["sku_jumbo"] != 0:
            c += 1
    return c, len(lista)

def debug_log(lista_de_productos):
    with open("debug_log.txt", "w") as file:

        now = datetime.now()
        curr = now.strftime("%H:%M")
        cant_matches , totales= matches_logrados(lista_de_productos)
        file.write("Hora: "+curr)
        file.write("\n")
        file.write("Cantidad de Matches: " + str(cant_matches))
        file.write("\n")
        file.write("Cantidad de productos: "+ str(totales))
        file.write("\n")
        miss = (cant_matches/totales)*100
        file.write("Miss rate: " + str(miss) + "%")
        file.write("\n")
        file.write("\n")
        file.write("Matched Products:\n")
        for elem in matched_products:
            n_tottus, n_jumbo = elem
            s_t = "Tottus: " + n_tottus
            s_j = "Jumbo: " + n_jumbo
            file.write(s_t)            
            file.write("\n")
            file.write(s_j)
            file.write("\n")
            file.write("\n")

    

# Funcion que actualiza los csvs producidos por el programa    
def update_csvs(lista_de_productos):
    lista_csv = []
    csv_to_list('main_core_product.csv', lista_csv)
    lista_og = []
    for elem in lista_csv:
        lista_og.append(elem[0])
    lista_nueva = []
    for elem in lista_de_productos:
        lista_nueva.append(elem['ean'])


    productos_por_agregar = list(set(lista_og)-set(lista_nueva))


    productos_nuevos = []
    cuantos_nuevos = 0
    for elem in lista_de_productos:
        for prod in productos_por_agregar:
            if elem["ean"] == prod:
                productos_nuevos.append(elem)
                cuantos_nuevos += 1
    
    print("De los ", len(lista_de_productos), " productos por agregar")
    print("Se encontro que ", cuantos_nuevos, " no estaban en la base de datos ")

    with open('main_core_product.csv', "a", encoding='UTF8', newline='') as main_products:
        writer = csv.writer(main_products)

        for product in productos_nuevos:
            data = [product['ean'], product['title'], product['exclusive'], product['description'], product['slug'], product['pack'], product['cant'], product['unit'], product['image'], product['brand'], product['img_link'], product['category_id']]
            writer.writerow(data)

    with open('main_core_skuprice.csv', 'a', encoding='UTF8', newline='') as file2:
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

    debug_log(lista_de_productos)

# Funcion para construir los archivos CSV a usar en la BD
def list_to_csv(lista_de_productos):
    # Hoja productos:
    with open('main_core_product.csv', "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        header = ['ean', 'title','exclusive','description','slug', 'pack','cant', 'unit','image','brand','url_img_ext', 'category_id' ]
        writer.writerow(header)

        for product in lista_de_productos:
            data = [product['ean'], product['title'], product['exclusive'], product['description'], product['slug'], product['pack'], product['cant'], product['unit'], product['image'], product['brand'], product['img_link'], product['category_id']]
            writer.writerow(data)
    
    with open('main_core_skuprice.csv', 'w', encoding='UTF8', newline='') as file2:
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

    debug_log(lista_de_productos)

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


    print("Nom1: ",nom1)
    print("Nom2: ",nom2)

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
        print("Cambio de nombre a: ", nom1)

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
        print("Cambio de nombre a: ",nom1)


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

    if per_1 >0.85:
        if per_2 > 0.5:
            print("nom1 in nom2")
            return True
    elif per_2 >0.85:
        if per_1 > 0.5:
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
    
    del palabras[pos_cant]
    del palabras[pos_unit-1]
    
    nombre = " ".join(palabras)

    return nombre, cant, unit


# funcion que retorna la informacion necesaria para adjuntar al producto, o False, "" y 0.
def buscar_producto_jumbo(producto, jumbo):
    nom = producto["title"]
    print()
    print()
    print("El nombre en tottus es: ", nom)
    marca = producto["brand"].lower()
    cantidad = producto["cant"]
    unit = producto["unit"].lower()
    link = producto["link_tottus"]
    print("Marca: ", marca)

    print("Link: ", link)
    # print("cantidad: ", cantidad)
    # print("unit: ", unit)

    

    for prod_jumbo in jumbo[1:]:
        brand_j = prod_jumbo[2].lower()
        titulo = prod_jumbo[0]
        

        title_j, cant_j, unit_j = extraer_unit_cant(titulo)
        link_j = prod_jumbo[1]

        if cant_j == cantidad and unit_j == unit:
            if brand_j == marca:
                print("link_jumbo", link_j)
                
                if nombres_similares(nom, title_j):
                    print()
                    print("Match confirmed")
                    SKU_j = prod_jumbo[-1][9:]
                    precio_j = "".join(prod_jumbo[4].strip("$").split("."))
                    
                    matched_products.append((nom, title_j))

                    return True, link_j, SKU_j, precio_j, 0
                print()
    if producto["sku_jumbo"] == 0:
        print("No hay match para: ", nom)

    return False, "", 0, 0, 1


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
    producto["category_id"] = ""
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


def del_tottus(tottus):
    lista_productos = []

    for i in range(len(tottus)):
        if (i == 0): continue   #skip header
        title = tottus[i][0]
        html_ean = tottus[i][1]
        marca_cant_unit = tottus[i][2].split("-")

        brand = marca_cant_unit[0].strip()
        cant = marca_cant_unit[1].strip().split(" ")[0]
        unit = marca_cant_unit[1].strip().split(" ")[1]

        ean_list = html_ean.split(" ")
        ean = ean_list[2][10:-1]        # data-ean="XXXXX"
        
        # print(title + "\t" + ean + "\t" + brand +"\t" + cant + "\t" + unit)

        prod_link = tottus[i][1]
        img_link = tottus[i][2]

        
        pre_cmr_price = tottus[i][5][1:-2].split(".")

        cmr_price = "".join(pre_cmr_price).strip()


        producto = ini_producto(ean, title, cant, unit, brand, prod_link, img_link, cmr_price)

        lista_productos.append(producto)
    return lista_productos


#   =============================================================
#                   Main Program
#   =============================================================

# GLOBALES
departamentos = {1: ["Aceites y Aderezos", "Snack", "Arroz"], 3:["Leche", "Yoghurt"], 6:["Cervezas"]}
departamentos_nombre = {1:"Despensa", 3:"Frescos y Lacteos", 6:"Bebidas y Licores"}

categorias = {"Arroz":6, "Snack":5, "Cervezas":2}

id_supermercado = {'lider': 1, 'tottus' : 2, 'jumbo':3}

matched_products = []

if __name__ == "__main__":
    lider = []
    jumbo = []
    tottus = []
    ean_tottus = []

    arroz_csv_jumbo = "To_scrap\Arroz-JumboData-ScrapeStorm.csv"
    arroz_csv_lider = 'To_scrap\Arroz-LiderData-ScrapeStorm.csv'
    arroz_csv_tottus = 'To_scrap\Arroz-TottusData-ScrapeStorm.csv'

    csv_to_list(arroz_csv_jumbo, jumbo)
    csv_to_list(arroz_csv_lider, lider)
    csv_to_list(arroz_csv_tottus, tottus)

    

    lista_productos = del_tottus(tottus)

    
    for producto in lista_productos:
        
        cond, link_j, SKU_j, precio_j, exclusivo = buscar_producto_jumbo(producto, jumbo)
        if cond:
            producto["link_jumbo"] = link_j
            producto["sku_jumbo"] = SKU_j
            producto["exclusive"] = exclusivo
            producto["price_j"] = precio_j

    update_csvs(lista_productos)




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

'''
14/02

Tengo que revisar que productos son encontrados y cuales no, escribiendo la lista_productos en un csv
tengo que devolver el valor exclusive = 0 cuando encuentre los productos en el jumbo
- lo mismo para el lider


15/02

Documentar como funciona un match entre productos

'''


 
