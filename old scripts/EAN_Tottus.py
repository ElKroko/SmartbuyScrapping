import csv

path_lista_productos = "To_scrap/lista_productos.csv"


def csv_tottus(filename, list):
    with open(filename, 'r') as file:
        csvr = csv.reader(file)
        with open(path_lista_productos, "w") as file2:
            for producto in csvr:
                list.append(producto)
                link = producto[1]
                file2.write(link + "\n")    # Creo un archivo para todos los links de los productos del tottus
                                        # Para buscar sus EAN en cada pagina particularme
if __name__ == "__main__":
    tottus = []
    ean_tottus = []

    csv_tottus("To_scrap/Tottus.csv", tottus)