#Jose David Santa Parra ----- 2241560 
#Brayan Tigreros ----- 2240825 

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

datos_hotel = "C:/Users/santa/Downloads/sistema_hotel.xlsx"

class Hotel:
    def __init__(self):
        self.df_habitaciones = pd.read_excel(datos_hotel, sheet_name="Habitaciones")
        self.df_clientes = pd.read_excel(datos_hotel, sheet_name="Clientes")
        self.df_reservas = pd.read_excel(datos_hotel, sheet_name="Reservas")

    def guardar_datos(self):
        with pd.ExcelWriter(datos_hotel) as writer:
            self.df_habitaciones.to_excel(writer, sheet_name="Habitaciones", index=False)
            self.df_clientes.to_excel(writer, sheet_name="Clientes", index=False)
            self.df_reservas.to_excel(writer, sheet_name="Reservas", index=False)

    def registrar_habitacion(self, numero, tipo, capacidad, precio, disponible=True):
        nueva_habitacion = {
            "ID_Habitacion": numero,
            "Tipo": tipo,
            "Capacidad": capacidad,
            "Precio_por_Noche": precio,
            "Disponible": disponible
        }
        self.df_habitaciones = pd.concat([self.df_habitaciones, pd.DataFrame([nueva_habitacion])], ignore_index=True)
        self.guardar_datos()

    def modificar_habitacion(self, numero, nuevo_precio=None, nueva_capacidad=None, nueva_disponibilidad=None):
        index = self.df_habitaciones[self.df_habitaciones["ID_Habitacion"] == numero].index
        if not index.empty:
            if nuevo_precio is not None:
                self.df_habitaciones.at[index[0], "Precio_por_Noche"] = nuevo_precio
            if nueva_capacidad is not None:
                self.df_habitaciones.at[index[0], "Capacidad"] = nueva_capacidad
            if nueva_disponibilidad is not None:
                self.df_habitaciones.at[index[0], "Disponible"] = nueva_disponibilidad
            self.guardar_datos()
        else:
            messagebox.showerror("Error", "Habitación no encontrada")

    def verificar_disponibilidad_habitacion(self, id_habitacion):
        habitacion = self.df_habitaciones[self.df_habitaciones["ID_Habitacion"] == id_habitacion]
        if not habitacion.empty:
            if habitacion["Disponible"].values[0]:
                return "La habitación está disponible."
            else:
                return "La habitación ya está en uso."
        else:
            return "Habitación no encontrada."

    def registrar_reserva(self, id_reserva, id_cliente, id_habitacion, fecha_inicio, fecha_fin):
        habitacion_disponible = self.df_habitaciones[
            (self.df_habitaciones["ID_Habitacion"] == id_habitacion) & 
            (self.df_habitaciones["Disponible"] == True) 
        ]
        if not habitacion_disponible.empty:
            nueva_reserva = {
                "ID_Reserva": id_reserva,
                "ID_Cliente": id_cliente,
                "ID_Habitacion": id_habitacion,
                "Fecha_Inicio": fecha_inicio,
                "Fecha_Fin": fecha_fin,
                "Estado": "Activa"
            }
            self.df_reservas = pd.concat([self.df_reservas, pd.DataFrame([nueva_reserva])], ignore_index=True)
            self.df_habitaciones.loc[self.df_habitaciones["ID_Habitacion"] == id_habitacion, "Disponible"] = False
            self.guardar_datos()
        else:
            messagebox.showerror("Error", "La habitación no está disponible o no existe")

    def modificar_reserva(self, id_reserva, nueva_fecha_inicio=None, nueva_fecha_fin=None):
        index = self.df_reservas[self.df_reservas["ID_Reserva"] == id_reserva].index
        if not index.empty:
            if nueva_fecha_inicio:
                self.df_reservas.at[index[0], "Fecha_Inicio"] = nueva_fecha_inicio
            if nueva_fecha_fin:
                self.df_reservas.at[index[0], "Fecha_Fin"] = nueva_fecha_fin
            self.guardar_datos()
        else:
            messagebox.showerror("Error", "Reserva no encontrada")

    def cancelar_reserva(self, id_reserva):
        index = self.df_reservas[self.df_reservas["ID_Reserva"] == id_reserva].index
        if not index.empty:
            id_habitacion = self.df_reservas.at[index[0], "ID_Habitacion"]
            self.df_reservas.at[index[0], "Estado"] = "Cancelada"
            self.df_habitaciones.loc[self.df_habitaciones["ID_Habitacion"] == id_habitacion, "Disponible"] = True
            self.guardar_datos()
        else:
            messagebox.showerror("Error", "Reserva no encontrada")

    def registrar_cliente(self, id_cliente, nombre, contacto, direccion):
        nuevo_cliente = {
            "ID_Cliente": id_cliente,
            "Nombre": nombre,
            "Contacto": contacto,
            "Direccion": direccion
        }
        self.df_clientes = pd.concat([self.df_clientes, pd.DataFrame([nuevo_cliente])], ignore_index=True)
        self.guardar_datos()

    def modificar_cliente(self, id_cliente, nuevo_nombre=None, nuevo_contacto=None, nueva_direccion=None):
     index = self.df_clientes[self.df_clientes["ID_Cliente"] == id_cliente].index
     if not index.empty:
        if nuevo_nombre:
            self.df_clientes.at[index[0], "Nombre"] = nuevo_nombre
        if nuevo_contacto:
            self.df_clientes.at[index[0], "Contacto"] = nuevo_contacto
        if nueva_direccion:
            self.df_clientes.at[index[0], "Direccion"] = nueva_direccion
        self.guardar_datos()
     else:
        messagebox.showerror("Error", "Cliente no encontrado")

    def obtener_historial_reservas(self, id_cliente):
        historial = self.df_reservas[self.df_reservas["ID_Cliente"] == id_cliente]
        return historial

    def reporte_ocupacion(self):
        ocupadas = self.df_reservas[self.df_reservas["Estado"] == "Activa"]
        fechas = ocupadas["Fecha_Inicio"]
        ocupacion_por_fecha = fechas.value_counts().sort_index()

        ocupacion_por_fecha.plot(kind="bar", color="#4EAA03")
        plt.title("Ocupación por fecha")
        plt.xlabel("Fecha")
        plt.ylabel("Cantidad de habitaciones ocupadas")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def reporte_ingresos(self, fecha_inicio, fecha_fin):
        reservas_periodo = self.df_reservas[
            (self.df_reservas["Fecha_Inicio"] >= fecha_inicio) & 
            (self.df_reservas["Fecha_Fin"] <= fecha_fin) & 
            (self.df_reservas["Estado"] == "Activa")
        ]
        ingresos = reservas_periodo.merge(self.df_habitaciones, on="ID_Habitacion")["Precio_por_Noche"].sum()
        messagebox.showinfo("Ingresos", f"Ingresos de reservas del {fecha_inicio} al {fecha_fin}: ${ingresos}")

    def analisis_demanda(self):
        tipos = self.df_reservas.merge(self.df_habitaciones, on="ID_Habitacion")["Tipo"].value_counts()
        tipos.plot(kind="bar", color="#FF9B42")
        plt.title("Demanda por tipo de habitación")
        plt.xlabel("Tipo de habitación")
        plt.ylabel("Cantidad de reservas")
        plt.tight_layout()
        plt.show()

class HotelApp:
    def __init__(self):
        self.hotel = Hotel()
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Reservas de Hotel")
        self.ventana.geometry("1250x700")
        self.ventana.resizable(0,0)
        self.ventana.config(bg="#CAF0FB")

    # FRAMES
        self.frame_izquierdo = tk.Frame(self.ventana,bg="#D0EDFC")
        self.frame_izquierdo.pack(side="left", padx=50, pady=20)

        self.frame_derecho = tk.Frame(self.ventana,bg="#D0EDFC")
        self.frame_derecho.pack(side="right", padx=50, pady=20)

        self.frame_medio = tk.Frame(self.ventana,bg="#D0EDFC")
        self.frame_medio.pack(side="top", padx=20, pady=40)

        self.frame_bajo = tk.Frame(self.ventana,bg="#D0EDFC")
        self.frame_bajo.pack(side="bottom", padx=5)

    # LABELS
        self.main_label = tk.Label(self.frame_medio,text="SISTEMA DE GESTION HOTELERA",font=("Arial",30),bg="#D0EDFC",fg="#3D0B60")
        self.main_label.pack(pady=30)

        self.label_left = tk.Label(self.frame_izquierdo, text="HABITACIONES", font=("Arial"),bg="#D0EDFC",fg="#C20000")
        self.label_left.pack(pady=5)

        self.label_right = tk.Label(self.frame_derecho, text="CLIENTES", font=("Arial"),bg="#D0EDFC",fg="#C20000")
        self.label_right.pack(pady=5)

        self.label_down = tk.Label(self.frame_bajo, text="REPORTES", font=("Arial"),bg="#D0EDFC",fg="#C20000")
        self.label_down.pack(pady=5)

        self.label_up = tk.Label(self.frame_medio, text="RESERVAS", font=("Arial"),bg="#D0EDFC",fg="#C20000")
        self.label_up.pack(pady=5)

    # ENTRYS
        self.entry_id_habitacion = self.create_entry(self.frame_izquierdo, "ID de la habitación:")
        self.entry_tipo_habitacion = self.create_entry(self.frame_izquierdo, "Tipo de habitación:")
        self.entry_capacidad_habitacion = self.create_entry(self.frame_izquierdo, "Capacidad de la habitación:")
        self.entry_precio_habitacion = self.create_entry(self.frame_izquierdo, "Precio por noche:")
        self.entry_disponibilidad_habitacion = self.create_entry(self.frame_izquierdo, "Disponibilidad (True/False):")
        
        self.entry_id_reserva = self.create_entry(self.frame_medio, "ID de reserva:")
        self.entry_id_cliente = self.create_entry(self.frame_medio, "ID de cliente:")
        self.entry_nueva_fecha_inicio = self.create_entry(self.frame_medio, "Nueva fecha de inicio (YYYY-MM-DD):")
        self.entry_nueva_fecha_fin = self.create_entry(self.frame_medio, "Nueva fecha de fin (YYYY-MM-DD):")

        self.entry_id_cliente_cliente = self.create_entry(self.frame_derecho, "ID del cliente:")
        self.entry_nombre_cliente = self.create_entry(self.frame_derecho, "Nombre del cliente:")
        self.entry_contacto_cliente = self.create_entry(self.frame_derecho, "Contacto del cliente:")
        self.entry_direccion_cliente = self.create_entry(self.frame_derecho, "Dirección del cliente:")

    # BOTONES
        self.button_registrar_cliente = tk.Button(self.frame_derecho, text="Registrar Cliente",font=('Arial',12), command=self.registrar_cliente,bg="#4EAA03",fg="white")
        self.button_registrar_cliente.pack(pady=5)

        self.button_modificar_cliente = tk.Button(self.frame_derecho, text="Modificar Cliente", font=('Arial',12),command=self.modificar_cliente,bg="#0077b6",fg="white")
        self.button_modificar_cliente.pack(pady=5)

        self.button_registrar_habitacion = tk.Button(self.frame_izquierdo, text="Registrar Habitación",font=('Arial',12), command=self.registrar_habitacion,bg="#4EAA03",fg="white")
        self.button_registrar_habitacion.pack(pady=5)

        self.button_modificar_habitacion = tk.Button(self.frame_izquierdo, text="Modificar Habitación",font=('Arial',12),command=self.modificar_habitacion,bg="#0077b6",fg="white")
        self.button_modificar_habitacion.pack(pady=5)

        self.button_verificar_disponibilidad = tk.Button(self.frame_izquierdo, text="Consultar Habitacion", font=("Arial",12), command=self.verificar_disponibilidad,bg="#FFFF72",fg="black")
        self.button_verificar_disponibilidad.pack(pady=5)

        self.button_registrar_reserva = tk.Button(self.frame_medio, text="Registrar Reserva",font=('Arial',12),command=self.registrar_reserva,bg="#4EAA03",fg="white")
        self.button_registrar_reserva.pack(pady=5)

        self.button_modificar_reserva = tk.Button(self.frame_medio, text="Modificar Reserva",font=('Arial',12), command=self.modificar_reserva,bg="#0077b6",fg="white")
        self.button_modificar_reserva.pack(pady=5)

        self.button_cancelar_reserva = tk.Button(self.frame_medio, text="Cancelar Reserva",font=('Arial',12), command=self.cancelar_reserva,bg="#FF4040",fg="white")
        self.button_cancelar_reserva.pack(pady=5)

    # BOTONES ESTADISTICAS
        self.button_reporte_ocupacion = tk.Button(self.frame_bajo, text="Reporte de Ocupación",font=('Arial',12), command=self.reporte_ocupacion,bg="#ECAB0F",fg="white")
        self.button_reporte_ocupacion.pack(pady=5)

        self.button_reporte_ingresos = tk.Button(self.frame_bajo, text="Reporte Ingresos",font=('Arial',12),command=self.reporte_ingresos,bg="#F7D547",fg="black")
        self.button_reporte_ingresos.pack(pady=5)

        self.button_analisis_demanda = tk.Button(self.frame_bajo, text="Analisis Demanda",font=('Arial',12),command=self.analisis_demanda,bg="#FFFF72",fg="black")
        self.button_analisis_demanda.pack(pady=5)

        tk.mainloop()

    def create_entry(self, ventana, label_text):
        label = tk.Label(ventana, text=label_text,font=('Arial',12),bg="#D0EDFC",fg="black")
        label.pack()
        entry = tk.Entry(ventana)
        entry.pack()
        return entry

    def registrar_habitacion(self):
        try:
            id_habitacion = int(self.entry_id_habitacion.get())
            tipo = self.entry_tipo_habitacion.get()
            capacidad = int(self.entry_capacidad_habitacion.get())
            precio = float(self.entry_precio_habitacion.get())
            disponible = self.entry_disponibilidad_habitacion.get().strip().lower() == 'true'
            self.hotel.registrar_habitacion(id_habitacion, tipo, capacidad, precio, disponible)
            messagebox.showinfo("Éxito", "Habitación registrada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese algun valor.")

    def modificar_habitacion(self):
        try:
            id_habitacion = int(self.entry_id_habitacion.get())
            nuevo_precio = float(self.entry_precio_habitacion.get()) if self.entry_precio_habitacion.get() else None
            nueva_capacidad = int(self.entry_capacidad_habitacion.get()) if self.entry_capacidad_habitacion.get() else None
            nueva_disponibilidad = self.entry_disponibilidad_habitacion.get().strip().lower() == 'true' if self.entry_disponibilidad_habitacion.get() else None
            self.hotel.modificar_habitacion(id_habitacion, nuevo_precio, nueva_capacidad, nueva_disponibilidad)
            messagebox.showinfo("Éxito", "Habitación modificada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese algun valor.")

    def verificar_disponibilidad(self):
        try:
            id_habitacion = int(self.entry_id_habitacion.get())
            resultado = self.hotel.verificar_disponibilidad_habitacion(id_habitacion)
            messagebox.showinfo("Disponibilidad", resultado)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID de habitación válido.")
            
    def registrar_reserva(self):
        try:
            id_reserva = int(self.entry_id_reserva.get())
            id_cliente = int(self.entry_id_cliente.get())
            id_habitacion = int(self.entry_id_habitacion.get())
            fecha_inicio = self.entry_nueva_fecha_inicio.get()
            fecha_fin = self.entry_nueva_fecha_fin.get()
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
            self.hotel.registrar_reserva(id_reserva, id_cliente, id_habitacion, fecha_inicio, fecha_fin)
            messagebox.showinfo("Éxito", "Reserva registrada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores para su reserva.")

    def modificar_reserva(self):
        try:
            id_reserva = int(self.entry_id_reserva.get())
            nueva_fecha_inicio = self.entry_nueva_fecha_inicio.get()
            nueva_fecha_fin = self.entry_nueva_fecha_fin.get()
            self.hotel.modificar_reserva(id_reserva, nueva_fecha_inicio, nueva_fecha_fin)
            messagebox.showinfo("Éxito", "Reserva modificada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese algun valor.")

    def cancelar_reserva(self):
        try:
            id_reserva = int(self.entry_id_reserva.get())
            self.hotel.cancelar_reserva(id_reserva)
            messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID de reserva valido.")

    def reporte_ocupacion(self):
        self.hotel.reporte_ocupacion()

    def analisis_demanda(self):
        self.hotel.analisis_demanda()

    def reporte_ingresos(self):
        try:
            fecha_inicio = self.entry_nueva_fecha_inicio.get()
            fecha_fin = self.entry_nueva_fecha_fin.get()
            datetime.strptime(fecha_inicio, '%Y-%m-%d')
            datetime.strptime(fecha_fin, '%Y-%m-%d')
            self.hotel.reporte_ingresos(fecha_inicio, fecha_fin)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese fechas en el formato YYYY-MM-DD.")

    def registrar_cliente(self):
        try:
            id_cliente = int(self.entry_id_cliente_cliente.get())
            nombre = self.entry_nombre_cliente.get()
            contacto = self.entry_contacto_cliente.get()
            direccion = self.entry_direccion_cliente.get()
            self.hotel.registrar_cliente(id_cliente, nombre, contacto, direccion)
            messagebox.showinfo("Éxito", "Cliente registrado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese algun valor.")

    def modificar_cliente(self):
        try:
            id_cliente = int(self.entry_id_cliente_cliente.get())
            nuevo_nombre = self.entry_nombre_cliente.get() or None
            nuevo_contacto = self.entry_contacto_cliente.get() or None
            nueva_direccion = self.entry_direccion_cliente.get() or None
            self.hotel.modificar_cliente(id_cliente, nuevo_nombre, nuevo_contacto, nueva_direccion)
            messagebox.showinfo("Éxito", "Cliente modificado correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese algun valor.")

app = HotelApp()