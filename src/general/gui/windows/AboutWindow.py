from src.general.gui.dialogs import TextDialog


__all__ = ["AboutWindow"]


class AboutWindow(TextDialog):
	def __init__(self):
		message = fr"""
			<h1>Виртуальные лабораторные работы по физике</h1>
			
			<h2>Разработчики:</h2>
			<ul>
				<li>Матвей Полубрюхов</li>
				<li></li>
			</ul>
			<p>Сборка v2.0.0<br/>
			Copyright &copy; 2023-2025 Матвей Полубрюхов</p>
		"""

		super().__init__(message, "О программе")
