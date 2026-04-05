import json

def agregar_recetas():
    recetas = optener_recetas()
    nombre = input("escribe un nombre")
    ingrediente1 = input("escribe un ingrediente")
    ingrediente2 = input("escribe otro ingrediente")
    
    if nombre.lower() == "si":
        nombre = nombre
    else:
        nombre= nombre
        
    recetas.append({"nombre" : nombre, "ingrediente1" : ingrediente1, "ingrediente2" : ingrediente2})
    
    
    with open("recetas.json", "w") as listas_recetas:
        json.dump(recetas, listas_recetas)
        
def lista_de_recetas():
    recetas = optener_recetas()
    for receta in recetas:
        print(f"{receta['nombre']} - {receta['ingrediente1']}- {receta['ingrediente2']}")
        
def optener_recetas():
        with open("recetas.json", "r") as archivo:
            recetas = json.load(archivo)
        return recetas
        return None
def eliminar_recetas():
    
    recetas = optener_recetas()
    nombre = input("eliminar receta")

    recetas_act = [ r for r in recetas if r ['nombre'].lower() != nombre.lower()]
    if len(recetas) ==
len(recetas_actualizadas):
print(f"no se encontro ninguna receta llamada '{nombre}' .")
    else:
    with open("recetas.json", "w") as archivo:
            json.dump(recetas_act, archivo, indent=4)
            print("la receta '{nombre}' ha sido eliminada")
    
    
    
    
        

        
