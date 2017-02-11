import os
from functools import partial
#from load_images import Load_Image
#from mlp import MultiLayerPerceptron as mlp

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

Window.size = (700, 450)

class MainWidget(TabbedPanel):
	_ListTrainingPictureClass1 = []
	_ListTrainingPictureClass2 = []

	_ListEvaluationPictureClass1 = []
	_ListEvaluationPictureClass2 = []

	_nameClass1 = ''
	_nameClass2 = ''

	''' Add MLP object '''
	# my_mlp = MLP()


	def __init__(self, **kwargs):
		super(MainWidget, self).__init__(**kwargs)


	''' Functions for the GUI '''
	def go_to_tab(self, index):
		tab = self.ids['tab_' + str(index)]
		self.switch_to(tab)

	
	''' Functions to load files '''
	def open_load_popup(self, side, type):
		content = GridLayout(cols=1, row_default_height=280, row_force_default=True)

		content_accept = Button(text='Accept', size_hint_y=None, height=40)
		content_cancel = Button(text='Cancel', size_hint_y=None, height=40)

		if type == 'test_image':
			file_chooser = FileChooserListView(id='chooser', filters=['*.jpg', '*.png'])
		else:
			file_chooser = FileChooserListView(id='chooser', filters=['*.jpg', '*.png'], dirselect=True)

		button_grid = GridLayout(cols=2, spacing=(10,10), padding=(10, 10))

		button_grid.add_widget(content_accept)
		button_grid.add_widget(content_cancel)
		
		content.add_widget(file_chooser)
		content.add_widget(button_grid)

		popup = Popup(title='Archivos',
					  size_hint=(None, None), 
					  size=(400, 400),
					  content=content)

		content_cancel.bind(on_release=popup.dismiss)
		content_accept.bind(on_release=partial(self.load_files, popup, side, type, file_chooser))

		popup.open()


	def load_files(self, popup, side, type, file_chooser, sender):
		path = file_chooser.selection

		if path == []:
			return

		if type == 'test_image':
			image_box = self.ids['image_box']
			image_box.source = path[0]
			image_box.reload()

		else:

			list_files = os.listdir(path[0])
			image_list = []

			for file in list_files:
				if os.path.isdir(file) == True:
					continue

				extension = os.path.splitext(file)[1]
				if  extension == '.jpg' or extension == '.png':
					image_list.append(path[0] + '\\' + file)


			if type == 'image_folder':
				label = self.ids['label_' + str(side) + '_training_path']

				if side == 'left':
					self._ListTrainingPictureClass1 = image_list
				elif side == 'right':
					self._ListTrainingPictureClass2 = image_list

			elif type == 'test_folder':
				label = self.ids['label_' + str(side) + '_test_path']

				if side == 'left':
					self._ListTrainingPictureClass1 = image_list
				else:
					self._ListTrainingPictureClass2 = image_list

			label.text = os.path.basename(path[0]) + ' -> ' + str(len(image_list)) + ' imagenes'

		popup.dismiss()
		

	''' Function to update class names in ''' 
	def change_class_name(self, side, text):
		label = self.ids['class_name_' + str(side)]
		label.text = text


	'''  Functions to setup MLP '''
	def create_training_set(self):
		training_set = []

		# Image proccesing
		'''
		for image in  self._ListTrainingPictureClass1:
			vector = Load_Image(image)
			training_set.append([vector, [1]])

		for image in self._ListTrainingPictureClass2:
			vector = Load_Image(image)
			training_set.append([vector, [-1]])
		'''

		return training_set

	def create_evaluation_set(self):
		evaluation_set = []

		# Image proccesing
		'''
		for image in self._ListEvaluationPictureClass1:
			vector = Load_Image(image)
			evaluation_set.append(vector)

		for image in self._ListEvaluationPictureClass2:
			vector = Load_Image(image)
			evaluation_set.append(vector)
		'''

		return evaluation_set

	def plot_roc_curve(self, mlp):
		pass

	''' Function for the MLP''' 
	def training(self):
		txt_architecture = self.ids['txt_architecture']
		txt_min_error = self.ids['txt_min_error']

		training_set = self.create_training_set()

		print training_set

		# Add elements to the MLP and training
		#self.my_mlp.min_error = float(txt_min_error.text)
		#self.my_mlp.txt_architecture = txt_architecture.text
		#self.my_mlp.training_set = training_set
		#self.my_mlp.training()

		self.go_to_tab(2)

	def evaluate_mlp(self):
		evaluation_set = self.create_evaluation_set()

		print evaluation_set

		#self.my_mlp.evualuation(evaluation_set)
		#self.plot_roc_curve(self.my_mlp)

		self.go_to_tab(3)

	def test_image(self):
		image_box = self.ids['image_box']

		if image_box.source == '':
			return
		
		#Load image and send to test
		'''
		test_image = Load_Image(image_box.source)
		result = self.my_mlp.test(test_image)

		label_result = self.ids['label_result']
		label_fit_class = self.ids['label_fit_class']

		label_result.text = str(result)

		if result >= 1:
			label_fit_class = self._nameClass1
		elif result < 1:
			label_fit_class = self._nameClass2

		'''

	''' Function to reset application '''
	def reset_mlp(self):

		self.ListTrainingPictureClass1 = []
		self._ListTrainingPictureClass2 = []
		self._ListEvaluationPictureClass1 = []
		self._ListEvaluationPictureClass2 = []
		self._nameClass1 = ''
		self._nameClass2 = ''
		#self.my_mlp = MLP()

		widget = self.ids['txt_class_1']
		widget.text = ''

		widget = self.ids['txt_class_2']
		widget.text = ''

		widget = self.ids['label_left_training_path']
		widget.text = ''

		widget = self.ids['label_right_training_path']
		widget.text = ''

		widget = self.ids['txt_min_error']
		widget.text = ''

		widget = self.ids['txt_architecture']
		widget.text = ''

		widget = self.ids['class_name_1']
		widget.text = ''

		widget = self.ids['class_name_2']
		widget.text = ''

		widget = self.ids['txt_class_2']
		widget.text = ''

		widget = self.ids['label_left_test_path']
		widget.text = ''

		widget = self.ids['label_right_test_path']
		widget.text = ''

		widget = self.ids['image_box']
		widget.source = ''
		widget.reload()

		widget = self.ids['label_result']
		widget.text = '--- Resultado ---'

		widget = self.ids['label_fit_class']
		widget.text = '--- Clase X ---'

		self.go_to_tab(1)


''' Class to construct the App '''
class MyApp(App):
	title = 'MLP'
	def build(self):
		return MainWidget()

if __name__ == '__main__':
	MyApp().run()