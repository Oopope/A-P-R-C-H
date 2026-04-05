recetas =["receta_1"]

receta1 = {
    "nombre" : "pizza" , "ingrediente1": "Pan", "ingrediente2": "queso"
}

recetas.append(receta1)

print(recetas)

recetas =["receta_2"]

receta2 = {
    "nombre" : "perros calientes" , "ingrediente1": "Pan", "ingrediente2" : "salchichas" 
}

recetas.append(receta2)

print(recetas)

recetas =["receta_3"]

receta3 = {
    "nombre" : "hamburguesa" , "ingrediente1": "Pan", "ingrediente2" : "carne"
}

recetas.append(receta3)

print(recetas)

recetass = []

def crear_receta(recetas):
    nombre = input("escribe un nombre").split("")
    ingrediente1 = input("escribe el primer ingrediente").split("")
    ingrediente2 = input("escribe el segundo ingrdiente").split("")
    
    receta1 = {
            "nombre" : "nombre",
            "ingrediente1" : "ingrediente1",
            "ingrediente2" : "ingrediente2"
               
    }
    
recetas.append(receta1)

crear_receta(recetass)

print(recetas)