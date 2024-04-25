import os
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext

# Buscar la palabra en los libros
def buscarPalabra():
    palabra = entradaPalabra.get().lower()  
    limpiarResultado()  
    librosEncontrados = []
    rutaLibros = r'C:\Users\VELA\Desktop\Recuperacion\Deber1\libros'
    for filename in os.listdir(rutaLibros):
        if filename.endswith('.txt'):
            with open(os.path.join(rutaLibros, filename), 'r', encoding='utf-8') as file:
                contenido = file.read()
                if palabra in contenido.lower():
                    librosEncontrados.append(filename)
    if librosEncontrados:
        resultadoText.config(state="normal")
        resultadoText.insert(tk.END, f"La palabra '{palabra}' se encuentra en los siguientes {len(librosEncontrados)} libros:\n{', '.join(librosEncontrados)}")
        resultadoText.config(state="disabled")
    else:
        messagebox.showinfo("Resultado", f"La palabra '{palabra}' no se encuentra en ningún libro.")

# Limpiar el contenido del resultado
def limpiarResultado():
    resultadoText.config(state="normal")
    resultadoText.delete(1.0, tk.END)
    resultadoText.config(state="disabled")

# Interfaz
root = tk.Tk()
root.title("Buscador de Palabras en Libros")

labelPalabra = tk.Label(root, text="Ingrese la palabra que desea buscar:")
labelPalabra.pack()

entradaPalabra = tk.Entry(root)
entradaPalabra.pack()

botonBuscar = tk.Button(root, text="Buscar", command=buscarPalabra)
botonBuscar.pack()

resultadoText = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
resultadoText.pack()

root.mainloop()
