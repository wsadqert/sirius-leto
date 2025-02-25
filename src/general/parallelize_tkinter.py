import multiprocessing
import threading
import tkinter as tk

def parallelize_tkinter(app: type | object, parallel_mode: str = "none") -> threading.Thread | multiprocessing.Process | None:
	"""
	parallel_mode: str - one of:
		`thread` - to run in separate thread
		`process` - to run in separate process
		`none` - run in main thread (default)
	"""

	def run_app():
		if getattr(app, "_run_app", None):
			app._run_app()
		else:
			if isinstance(app, type):
				# is class
				root = tk.Tk()
				_app = app(root)
				root.mainloop()
			
			elif isinstance(app, tk.Tk):
				# is object
				app.mainloop()

	match parallel_mode:
		case "thread":
			thread = threading.Thread(target=run_app)
			thread.start()
			return thread

		case "process":
			process = multiprocessing.Process(target=run_app)
			process.start()
			return process

		case "none":
			run_app()
		
		case _:
			raise ValueError
