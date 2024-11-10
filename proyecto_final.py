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

    def consultar_habitaciones_disponibles(self, tipo=None, precio_max=None):
        disponibles = self.df_habitaciones[self.df_habitaciones["Disponible"] == True]
        if tipo:
            disponibles = disponibles[disponibles["Tipo"] == tipo]
        if precio_max:
            disponibles = disponibles[disponibles["Precio_por_Noche"] <= precio_max]
        return disponibles

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

    def obtener_historial_reservas(self, id_cliente):
        historial = self.df_reservas[self.df_reservas["ID_Cliente"] == id_cliente]
        return historial

    def reporte_ocupacion(self):
        ocupadas = self.df_reservas[self.df_reservas["Estado"] == "Activa"]
        fechas = ocupadas["Fecha_Inicio"]
        plt.plot(fechas.value_counts().sort_index())
        plt.title("Ocupación por fecha")
        plt.xlabel("Fecha")
        plt.ylabel("Ocupación")
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
        tipos.plot(kind="bar")
        plt.title("Demanda por tipo de habitación")
        plt.xlabel("Tipo de Habitación")
        plt.ylabel("Reservas")
        plt.show()

class HotelApp:
    def __init__(self):
        self.hotel = Hotel()
        self.ventana = tk.Tk()
        self.ventana.title("Sistema de Reservas de Hotel")

        self.entry_id_habitacion = self.create_entry(self.ventana, "ID de la habitación:")
        self.entry_tipo_habitacion = self.create_entry(self.ventana, "Tipo de habitación:")
        self.entry_capacidad_habitacion = self.create_entry(self.ventana, "Capacidad de la habitación:")
        self.entry_precio_habitacion = self.create_entry(self.ventana, "Precio por noche:")
        self.entry_disponibilidad_habitacion = self.create_entry(self.ventana, "Disponibilidad (True/False):")
        
        self.entry_id_reserva = self.create_entry(self.ventana, "ID de reserva:")
        self.entry_id_cliente = self.create_entry(self.ventana, "ID de cliente:")
        self.entry_nueva_fecha_inicio = self.create_entry(self.ventana, "Nueva fecha de inicio (YYYY-MM-DD):")
        self.entry_nueva_fecha_fin = self.create_entry(self.ventana, "Nueva fecha de fin (YYYY-MM-DD):")

        self.button_registrar_habitacion = tk.Button(self.ventana, text="Registrar Habitación", command=self.registrar_habitacion)
        self.button_registrar_habitacion.pack()

        self.button_modificar_habitacion = tk.Button(self.ventana, text="Modificar Habitación", command=self.modificar_habitacion)
        self.button_modificar_habitacion.pack()

        self.button_registrar_reserva = tk.Button(self.ventana, text="Registrar Reserva", command=self.registrar_reserva)
        self.button_registrar_reserva.pack()

        self.button_modificar_reserva = tk.Button(self.ventana, text="Modificar Reserva", command=self.modificar_reserva)
        self.button_modificar_reserva.pack()

        self.button_cancelar_reserva = tk.Button(self.ventana, text="Cancelar Reserva", command=self.cancelar_reserva)
        self.button_cancelar_reserva.pack()

        self.button_reporte_ocupacion = tk.Button(self.ventana, text="Reporte de Ocupación", command=self.reporte_ocupacion)
        self.button_reporte_ocupacion.pack()

        tk.mainloop()

    def create_entry(self, ventana, label_text):
        label = tk.Label(ventana, text=label_text)
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
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

    def modificar_habitacion(self):
        try:
            id_habitacion = int(self.entry_id_habitacion.get())
            nuevo_precio = float(self.entry_precio_habitacion.get()) if self.entry_precio_habitacion.get() else None
            nueva_capacidad = int(self.entry_capacidad_habitacion.get()) if self.entry_capacidad_habitacion.get() else None
            nueva_disponibilidad = self.entry_disponibilidad_habitacion.get().strip().lower() == 'true' if self.entry_disponibilidad_habitacion.get() else None
            self.hotel.modificar_habitacion(id_habitacion, nuevo_precio, nueva_capacidad, nueva_disponibilidad)
            messagebox.showinfo("Éxito", "Habitación modificada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

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
            messagebox.showerror("Error", "Por favor, ingrese valores válidos o verifique el formato de la fecha.")

    def modificar_reserva(self):
        try:
            id_reserva = int(self.entry_id_reserva.get())
            nueva_fecha_inicio = self.entry_nueva_fecha_inicio.get()
            nueva_fecha_fin = self.entry_nueva_fecha_fin.get()
            self.hotel.modificar_reserva(id_reserva, nueva_fecha_inicio, nueva_fecha_fin)
            messagebox.showinfo("Éxito", "Reserva modificada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos.")

    def cancelar_reserva(self):
        try:
            id_reserva = int(self.entry_id_reserva.get())
            self.hotel.cancelar_reserva(id_reserva)
            messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese un ID de reserva válido.")

    def reporte_ocupacion(self):
        self.hotel.reporte_ocupacion()

app = HotelApp()