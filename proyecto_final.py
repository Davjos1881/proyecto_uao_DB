import tkinter as tk
from tkinter import messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Habitacion:
    def _init_(self, numero, tipo, capacidad, precio, estado='Libre'):
        self.numero = numero
        self.tipo = tipo
        self.capacidad = capacidad
        self.precio = precio
        self.estado = estado

class Cliente:
    def _init_(self, nombre, direccion, contacto):
        self.nombre = nombre
        self.direccion = direccion
        self.contacto = contacto
        self.historial_reservas = []

class Reserva:
    def _init_(self, cliente, habitacion, fecha_inicio, fecha_fin):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

class SistemaHotel:
    def _init_(self):
        self.habitaciones = []
        self.clientes = []
        self.reservas = []
