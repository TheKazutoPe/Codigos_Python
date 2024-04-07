import psutil
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import datetime
import locale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from tkinter import filedialog
from tkinter import messagebox
import time

locale.setlocale(locale.LC_ALL, '')  # Para establecer la fecha y hora de la region actual


class StatsCPU:
    def init(self, master):  # Creamos la clase StatsCPU
        self.master = master
        self.master.geometry("600x310")  # Definimos su tamaño
        self.master.resizable(0, 0)  # Evitamos que se pueda modificar el tamaño

        # Wireframe

        self.master.title("Monitor de recursos")
        frmCPU = tk.Frame(self.master)
        frmCPU.place(x=10, y=55)

        # Menu Bar
        menu_bar = tk.Menu(self.master)  # Creamos el menu bar
        self.master.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Registro CSV", menu=file_menu)  # Creamos nuestra lista de opciones
        file_menu.add_command(label="Iniciar captura", command=self.iniciar_captura)  # Incluimos las opciones
        file_menu.add_command(label="Detener captura", command=self.detener_captura)

        # FRAME RAM
        frmRAM = tk.Frame(self.master)
        frmRAM.place(x=10, y=110)

        # FRAME DISCO DURO
        frmHDD = tk.Frame(self.master)
        frmHDD.place(x=10, y=170)

        # FRAME STATUS BAR
        frmST = tk.LabelFrame(self.master)
        frmST.place(x=0, y=275, width=600)

        # FRAME GRAFICA
        frmGrafica = tk.Frame(self.master)
        frmGrafica.place(x=300, y=20)

        self.actualizar_cpu()  # Obtenemos las estadisticas del CPU, RAM y HDD

        # Monitor 1
        self.CPU = tk.Label(frmCPU, text=f" CPU Usage ( {self.coretotal:2} core):  {self.cpu:3}%")
        self.CPU.grid(row=0, column=0, padx=3, pady=3)
        self.monitor1 = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=250)
        self.monitor1.place(x=20, y=80)
        self.monitor1.step(self.cpu)

        # Monitor 2
        self.RAM = tk.Label(frmRAM, text=f" RAM Usage (Total {self.ramtotal:.1f}Gb): {self.ram:3}%")
        self.RAM.grid(row=0, column=0, padx=3, pady=3)
        self.monitor2 = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=250)
        self.monitor2.place(x=20, y=135)
        self.monitor2.step(self.ram)

        # Monitor 3
        self.HDD = tk.Label(frmHDD, text=f" HDD Usage (Total {self.HT:.2f}Gb ): {self.hdd:.2f}%")
        self.HDD.grid(row=0, column=0, padx=3, pady=3)
        self.monitor3 = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=250)
        self.monitor3.place(x=20, y=195)
        self.monitor3.step(self.hdd)

        # STATUS BAR - NET INFO
        self.NET = tk.Label(frmST, text=f"Net info [in:{self.net_recv} | out:{self.net_sent}]")
        self.NET.grid(row=0, column=0, padx=5, pady=5)

        # STATUS BAR - FECHA
        self.DATE = tk.Label(frmST, text=f"{self.ram}")
        self.DATE.grid(row=0, column=1, padx=240, pady=5)

        # GRAFICA
        self.fig, self.ax = plt.subplots(figsize=(4, 3.5), facecolor="#F0F0ED")
        self.ax.set_title("CPU Usage [%]")
        self.x = np.arange(0, 50)
        self.y = np.zeros(50)
        self.ax.set_ylim(0, 105)
        self.line, = self.ax.plot(self.x, self.y, "blue")
        self.ax.tick_params(colors='#F0F0ED', axis='x')
        self.ax.grid(linestyle=":")
        self.graph = FigureCanvasTkAgg(self.fig, master=frmGrafica)
        self.graph.get_tk_widget().pack(fill=tk.X)

        self.actualizar_monitor()  # Actualiza los estados de los monitores
        self.actualizar_grafica()  # Actualiza la grafica

        global archivo_csv
        archivo_csv = None

    def iniciar_captura(self):
        global archivo_csv
        # Abrir ventana de dialogo para seleccionar archivo CSV
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if nombre_archivo:
            archivo_csv = open(nombre_archivo, mode='w', newline='')
            # Crear el objeto CSV writer y escribir la cabecera
            writer = csv.writer(archivo_csv, delimiter=';')

            while archivo_csv is not None:
                a = psutil.cpu_count(logical=False)
                self.actualizar_cpu()
                writer.writerow(["time", "cpu", "memory", "disk", "net"])
                writer.writerow(["-", f"{a} core", f"{self.ramtotal:.2f}G", f"{self.HT:.2f}", "-"])
                writer.writerow(
                    [f"{self.realtime}", f"{self.cpu}%%", f"{self.ram}%%", f"{self.hdd}%%", f"in: {self.net_recv}",
                     f"out: {self.net_sent}"])
                writer.writerow([])
                writer.writerow([])
                time.sleep(1)

    def detener_captura(self):
        global archivo_csv
        if archivo_csv is not None:

            archivo_csv.close()
            messagebox.showinfo("Captura finalizada", "La captura ha finalizado correctamente.")
            archivo_csv = None

        else:
            messagebox.showwarning("Archivo no abierto", "No hay ningún archivo CSV abierto.")

    def actualizar_cpu(self):
        self.cpu = psutil.cpu_percent()  # Se obtiene el porcentaje de uso del CPU
        self.ram = psutil.virtual_memory().percent  # Se obtiene el porcentaje de uso de la RAM
        self.ramtotal = psutil.virtual_memory().total / 1024 / 1024 / 1024  # Se obtiene la RAM disponible en gigabytes
        self.coretotal = psutil.cpu_count(logical=False)  # Se obtiene el numero de nucleros de CPU
        self.hdd = psutil.disk_usage("/").percent  # Se obtiene el porcentaje del disco duro
        self.HT = psutil.disk_usage(
            "/").total / 1024 / 1024 / 1024  # Se obtiene la capacidad de disco duro en gigabytes
        self.net_recv = psutil.net_io_counters().bytes_recv  # Se obtiene la cantidad de bytes recibidos
        self.net_sent = psutil.net_io_counters().bytes_sent  # Se obtiene la cantidad de bytes enviados
        self.realtime = datetime.datetime.now().strftime("%F %T")  # Se obtiene la fecha y hora actual

    def actualizar_grafica(self):
        self.actualizar_cpu()  # Obtenemos las estadisticas del CPU, RAM y HDD
        self.y = np.delete(self.y, 0)  # Se eliminan los elementos antiguos
        self.y = np.append(self.y, self.cpu)  # Se agregan los nuevos elementos de 'y'
        self.line.set_ydata(self.y)  # Se actualiza los datos de la linea para 'y'
        self.graph.draw()  # Se actualiza la grafica
        self.master.after(1000,
                          self.actualizar_grafica)  # Espera 1000 milisegundos antes de volver a llamar la funcion 'updateGrafica'

    def actualizar_monitor(self):
        self.actualizar_cpu()  # Obtenemos las estadisticas del CPU, RAM y HDD
        # Imprimimos las estadisticas
        self.CPU.config(text=f" CPU Usage ({self.coretotal:0} core): {self.cpu:3}%")
        self.RAM.config(text=f" RAM Usage Total({self.ramtotal:.1f}Gb): {self.ram:3}%")
        self.HDD.config(text=f" HDD Usage Total({self.HT:.2f}Gb ): {self.hdd:.2f}%")
        self.NET.config(
            text=f" Net info [in:{locale.format('%d', self.net_recv, 1)} | out:{locale.format('%d', self.net_sent, 1)}]",
            anchor="nw")
        self.DATE.config(text=f"{self.realtime}", anchor="se")

        self.monitor1.step(self.cpu)  # Actualiza el monitor 1
        self.monitor1.stop()  # Pausa el widget
        self.monitor1.step(self.cpu)  # Vuelve a actualizar el monitor 1

        self.monitor2.step(self.ram)  # Actualiza el monitor 2
        self.monitor2.stop()  # Pausa el widget
        self.monitor2.step(self.ram)  # Vuelve a actualizar el monitor 2

        self.monitor3.step(self.hdd)  # Actualiza el monitor 3
        self.monitor3.stop()  # Pausa el widget
        self.monitor3.step(self.hdd)  # Vuelve a actualizar el monitor 3

        self.master.after(1000, self.actualizar_monitor)  # Espera 1000 milisegundos antes de volver a actualizar

        # Pantalla de mosaico
        log_str = "|---------------------|----------|----------|----------|-----------------------------|\n"
        log_str += "|---------time--------|---cpu----|--memory--|---disk---|-------------net-------------|\n"
        log_str += "|                     |  {}core  | {:.2f}G |  {:.2f}  |                             |\n".format(
            psutil.cpu_count(logical=False), self.ramtotal, self.HT)
        log_str += "| {} |   {}%%  |   {}%%  |   {}%%  | in:{} out:{} |\n".format(self.realtime,
                                                                                  self.cpu, self.ram,
                                                                                  self.hdd,
                                                                                  self.net_recv,
                                                                                  self.net_sent)
        print(log_str)


root = tk.Tk()
app=StatsCPU(root)
root.mainloop()


