import tkinter as tk
from tkinter import messagebox, ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HydraulicBlackBoxApp:
	def __init__(self) -> None:
		self.num_vessels: int = 5
		self.inf_height: float = 10000000000.0
		self.vessel_areas: list[float] = [1.0, 2.0, 5.0, 3.0, 4.0]
		self.vessel_heights: list[float] = [2.0, 5.0, 8.0, 3.0, self.inf_height]
		self.max_water: float = 55.0
		self.attempts: int = 0

		self.vessel_combo = None
		self.area_entries = []
		self.link_entries = []
		self.canvas_vessels = None
		self.ax = None
		self.root = None
		self.water_entry = None
		self.volume_label = None
		self.area_frame = None
		self.conn_frame = None
		self.radio_frame = None

		self.connections = self.make_connections(self.num_vessels)

	# соединения между сосудами
	def make_connections(self, n: int) -> dict[int, list[tuple[int, float]]]:
		connections = {i: [] for i in range(n)}
		for i in range(n - 1):
			link_height = random.uniform(1.0, 8.0)
			connections[i].append((i + 1, link_height))
			connections[i + 1].append((i, link_height))
		return connections
	
	# счёт уровней воды в сосудах
	def calc_water_levels(self, water_amount: float) -> list[float]:
		levels = [0] * self.num_vessels
		water_left = water_amount
		sorted_vessels = sorted(range(self.num_vessels), key=lambda i: self.vessel_heights[i])
		for i in sorted_vessels:
			if water_left <= 0:
				break
			connected_vessels = [i]
			total_area = self.vessel_areas[i]
			min_height = self.vessel_heights[i]
			for j, link_height in self.connections[i]:
				if self.vessel_heights[j] <= link_height:
					connected_vessels.append(j)
					total_area += self.vessel_areas[j]
					min_height = min(min_height, self.vessel_heights[j])
			delta_height = min(water_left / total_area, min_height)
			for j in connected_vessels:
				levels[j] += delta_height
			water_left -= delta_height * total_area
		return levels

	# ЛЮБИМИ ГРАФИК (нет)
	def draw_graph(self) -> None:
		volumes = []
		heights = []
		for volume in range(0, int(self.max_water) + 1):
			levels = self.calc_water_levels(volume)
			total_height = sum(levels)
			volumes.append(volume)
			heights.append(total_height)
		self.ax.clear()

		self.ax.plot(volumes, heights, marker='o', linestyle='-', color='b')
		self.ax.set_title("Зависимость объёма от высоты столба жидкости")
		self.ax.set_xlabel("Объем жидкости (л)")
		self.ax.set_ylabel("Высота столба жидкости (м)")
		self.ax.grid(True)
		self.ax.set_xticks(range(0, int(self.max_water) + 1, 5))
		max_height = max(heights)
		self.ax.set_yticks([i for i in range(0, int(max_height) + 2, 1)])
		for i in range(self.num_vessels - 1):
			link_height = self.connections[i][0][1]
			self.ax.axhline(y=link_height, color='r', linestyle='--')
		current_volume = float(self.water_entry.get()) if self.water_entry.get() else 0

		water_levels = self.calc_water_levels(current_volume)
		for i in range(self.num_vessels):
			self.ax.scatter(current_volume, water_levels[i], color='red', zorder=5)
			self.ax.text(current_volume, water_levels[i], f'{i}', verticalalignment='bottom', horizontalalignment='right', color='black', fontsize=12, zorder=6)
		self.canvas.draw()

	# уровни воды в сосудах
	def show_water_levels(self, water_amount: float) -> None:
		water_levels = self.calc_water_levels(water_amount)
		if water_levels is None:
			messagebox.showwarning("Error", "Объем слишком большой!!")
			return
		self.canvas_vessels.delete("all")

		for j in range(self.num_vessels):
			water_height = water_levels[j] * 20
			self.canvas_vessels.create_rectangle(80 + j * 100, 50, 160 + j * 100, 200, outline="black", width=2)
			self.canvas_vessels.create_rectangle(80 + j * 100, 200 - water_height, 160 + j * 100, 200, fill="lightblue")
		for i in range(0, 151, 30):
			self.canvas_vessels.create_line(60, 200 - i, 80, 200 - i, width=2)
			self.canvas_vessels.create_text(50, 200 - i, text=f"{i/20:.2f}")
		self.volume_label.config(text=f"Объем воды: {water_amount:.2f}")

		self.root.update()

	# обновляем уровни воды
	def update_water_levels(self) -> None:
		try:
			water_amount = float(self.water_entry.get())
			if water_amount > self.max_water:
				messagebox.showwarning("Error", f"Максимальный объем жидкости: {self.max_water}")
				return
			if water_amount < 0:
				messagebox.showwarning("Error", "Объем не может быть отрицательным! :(")
				return
			self.show_water_levels(water_amount)
			self.draw_graph()
		except ValueError:
			messagebox.showwarning("Error", "Введи число!")

	# проверяем площади
	def check_areas(self) -> None:
		try:
			user_areas = [round(float(self.area_entries[i].get()), 1) for i in range(self.num_vessels)]
			water_amount = float(self.water_entry.get())
			correct_areas = [round(water_amount / h, 1) if h != 0 else 0 for h in self.calc_water_levels(water_amount)]
			if user_areas == correct_areas:
				messagebox.showinfo("Result", "Площади введены правильно! :)")
				self.show_water_levels(water_amount)
				self.check_filled_vessels()
			else:
				self.attempts += 1
				if self.attempts >= 7:
					messagebox.showinfo("Result", f"Правильные площади: {correct_areas}")
				else:
					messagebox.showinfo("Result", "Площади введены неправильно! Попробуй еще раз ;)")
		except ValueError:
			messagebox.showwarning("Error", "Введи числа для всех площадей!")

	# проверяем кол-во заполненных сосудов
	def check_filled_vessels(self) -> None:
		user_answer = int(self.vessel_combo.get())
		filled_vessels = sum(1 for h in self.calc_water_levels(float(self.water_entry.get())) if h > 0)
		if user_answer == filled_vessels:
			messagebox.showinfo("Result", "Правильно! Все сосуды отображены. :0")
			self.check_connections()
		else:
			self.attempts += 1
			if self.attempts >= 7:
				messagebox.showinfo("Result", f"Правильное количество заполненных сосудов: {filled_vessels}")
			else:
				messagebox.showinfo("Result", "Неправильно, попробуй еще раз! ;)")

	# проверяем высоты перемычек
	def check_connections(self) -> None:
		try:
			user_connections = [round(float(self.link_entries[i].get()), 1) for i in range(self.num_vessels - 1)]
			correct_connections = [round(self.connections[i][0][1], 1) for i in range(self.num_vessels - 1)]
			if user_connections == correct_connections:
				messagebox.showinfo("Result", "Высоты перемычек введены правильно! :)")
			else:
				self.attempts += 1
				if self.attempts >= 7:
					messagebox.showinfo("Result", f"Правильные высоты перемычек: {correct_connections}")
				else:
					messagebox.showinfo("Result", "Высоты перемычек введены неправильно! Попробуй еще раз ;)")
		except ValueError:
			messagebox.showwarning("Error", "Введи числа для всех перемычек!")

	# плюс сосуд
	def add_vessel(self) -> None:
		self.num_vessels += 1
		self.vessel_areas.append(random.uniform(1.0, 5.0))
		self.vessel_heights.append(random.uniform(1.0, 10.0))
		self.connections = self.make_connections(self.num_vessels)
		self.update_interface()

	# делит сосудик
	def remove_vessel(self) -> None:
		if self.num_vessels > 1:
			self.num_vessels -= 1
			self.vessel_areas.pop()
			self.vessel_heights.pop()
			self.connections = self.make_connections(self.num_vessels)
			self.update_interface()
		else:
			messagebox.showwarning("Error", "Нельзя удалить все сосуды!!")

	# обновляем комбобокс (английский для слабых) для выбора количества заполненных сосудов
	def update_radio_buttons(self) -> None:
		for widget in self.radio_frame.winfo_children():
			widget.destroy()
		tk.Label(self.radio_frame, text="Количество заполненных сосудов:", font=("Garamond", 12)).grid(row=0, column=0, padx=5, pady=5)

		self.vessel_combo = ttk.Combobox(self.radio_frame, values=[str(i) for i in range(self.num_vessels + 1)], font=("Garamond", 12), width=10)
		self.vessel_combo.grid(row=0, column=1, padx=5, pady=5)
		self.vessel_combo.set("0")

	# обновляем интерфейс
	def update_interface(self) -> None:
		for widget in self.area_frame.winfo_children():
			widget.destroy()
		area_labels = [f"Площадь сосуда {i}" for i in range(self.num_vessels)]

		self.area_entries = [tk.Entry(self.area_frame, font=("MS Sans Serif", 12), width=10) for _ in range(self.num_vessels)]
		for i in range(self.num_vessels):
			tk.Label(self.area_frame, text=area_labels[i], font=("Garamond", 12)).grid(row=i // 2, column=(i % 2) * 2, padx=10, pady=5)
			self.area_entries[i].grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
		for widget in self.conn_frame.winfo_children():
			widget.destroy()
		conn_labels = [f"Высота перемычки {i}-{i+1}" for i in range(self.num_vessels - 1)]
		
		self.link_entries = [tk.Entry(self.conn_frame, font=("MS Sans Serif", 12), width=10) for _ in range(self.num_vessels - 1)]
		for i in range(self.num_vessels - 1):
			tk.Label(self.conn_frame, text=conn_labels[i], font=("Garamond", 12)).grid(row=i // 2, column=(i % 2) * 2, padx=10, pady=5)
			self.link_entries[i].grid(row=i // 2, column=(i % 2) * 2 + 1, padx=10, pady=5)
		self.update_radio_buttons()
		self.draw_graph()
		self.show_water_levels(float(self.water_entry.get()) if self.water_entry.get() else 0)

	def _run_app(self) -> None:
		# само окно
		self.root = tk.Tk()
		self.root.title("Гидравлический чёрный ящик-ик")
		self.root.geometry("1400x800")

		# панель управления
		control_frame = tk.Frame(self.root)
		control_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		self.water_entry = tk.Entry(control_frame, font=("MS Sans Serif", 14))
		self.water_entry.grid(row=0, column=0, columnspan=2, pady=10)
		btn = tk.Button(control_frame, text="Влить воду", command=self.update_water_levels, font=("Arial", 12), bg="lightblue")
		btn.grid(row=1, column=0, columnspan=2, pady=5)
		add_btn = tk.Button(control_frame, text="Добавить сосуд", command=self.add_vessel, font=("Arial", 12), bg="lightgreen")
		add_btn.grid(row=2, column=0, pady=5)
		remove_btn = tk.Button(control_frame, text="Удалить сосуд", command=self.remove_vessel, font=("Arial", 12), bg="salmon")
		remove_btn.grid(row=2, column=1, pady=5)

		# площади
		self.area_frame = tk.Frame(control_frame)
		self.area_frame.grid(row=3, column=0, columnspan=2, pady=10)
		check_area_btn = tk.Button(control_frame, text="Проверить площади", command=self.check_areas, font=("Arial", 12), bg="orange")
		check_area_btn.grid(row=4, column=0, columnspan=2, pady=10)

		# перемычки
		self.conn_frame = tk.Frame(control_frame)
		self.conn_frame.grid(row=5, column=0, columnspan=2, pady=10)
		check_conn_btn = tk.Button(control_frame, text="Проверить перемычки", command=self.check_connections, font=("Arial", 12), bg="pink")
		check_conn_btn.grid(row=6, column=0, columnspan=2, pady=10)

		max_values_frame = tk.Frame(control_frame)
		max_values_frame.grid(row=7, column=0, columnspan=2, pady=10)
		tk.Label(max_values_frame, text="Максимальные значения:", font=("Garamond", 14, "bold")).grid(row=0, column=0, columnspan=2)
		tk.Label(max_values_frame, text=f"Максимальный объем: {self.max_water} л", font=("Garamond", 12)).grid(row=1, column=0, columnspan=2)
		tk.Label(max_values_frame, text=f"Максимальная высота: {max(self.vessel_heights)} м", font=("Garamond", 12)).grid(row=2, column=0, columnspan=2)
		self.volume_label = tk.Label(control_frame, text=f"Объем воды: {0:.2f}", font=("Garamond", 14, "bold"))

		self.volume_label.grid(row=8, column=0, columnspan=2, pady=5)

		# сосуды
		self.radio_frame = tk.Frame(control_frame)
		self.radio_frame.grid(row=9, column=0, columnspan=2, pady=10)
		self.update_radio_buttons()
		self.canvas_vessels = tk.Canvas(self.root, width=900, height=300, bg="white")
		self.canvas_vessels.grid(row=1, column=0, columnspan=2, pady=10)

		# график
		fig, self.ax = plt.subplots(figsize=(8, 6))
		self.canvas = FigureCanvasTkAgg(fig, master=self.root)
		self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=10, padx=10, pady=10, sticky="nsew")
		self.update_interface()
		self.root.grid_rowconfigure(0, weight=1)
		self.root.grid_columnconfigure(0, weight=1)
		self.root.grid_columnconfigure(1, weight=1)
		self.root.grid_columnconfigure(2, weight=3)

		# по-братски пускай запустится, я уже не знаю, плиз
		self.root.mainloop()

# HydraulicBlackBoxApp()._run_app()
