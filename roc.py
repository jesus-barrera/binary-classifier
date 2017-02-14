import matplotlib.pyplot as plt

class ROC():
    def __init__(self):
        self._figure = plt.figure()
        self._axes = self._figure.add_subplot(111)

        self._axes.set_xlabel('Especificidad')
        self._axes.set_ylabel('Sensibilidad')

        self._axes.set_xlim(0, 1)
        self._axes.set_ylim(0, 1)

        self._curve, = self._axes.plot([], [], 'b-')

    def plot(self, especificity, sensibility):
        self._curve.set_data(especificity, sensibility)
        self._figure.canvas.draw()
