#inicio

import funciones as modulo_recetas

def menu():
    print()
    print ("1 agregar recetas")
    print()
    print("2 listas de recetas")
    print()
    print("3 eliminar recetas")
    print()
    print("4 salir")
    
    
def datos_recetas():
    nombre = input("ingrese un nombre")
    ingrediente1 = input("ingrese un ingrediente")
    ingrediente2 = input("ingrese otro ingrediente")
    
    return {"nombre" : nombre, "ingrediente1" : ingrediente1, "ingrediente2": ingrediente2, }
print("sistema de recetas de cocina")
print()

while True:
    menu()
    
    opcion= input("seleccione una opcion")
    match opcion:
        case "1":
            recetas = datos_recetas()
            modulo_recetas.agregar_recetas()
            print("receta agregada")
            print()
        case "2":
            modulo_recetas.lista_de_recetas()
            print("listas de recetas")
            print()
        case "3":
            modulo_recetas.eliminar_recetas()
            print("eliminar recetas")
            print()
        case "4":
            print("salir")
            break
        case _:
            print("opcion invalida")
            
        
    
    









    
    
    

          
    
    
