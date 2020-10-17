import matplotlib.pyplot as plt


class Gerador:
    def __init__(self):
        pass

    @staticmethod
    def variable_length(size_data, error_data):
        fig, ax = plt.subplots()
        plt.plot(size_data, error_data, "ro", size_data, error_data, "k")
        for i, txt in enumerate(error_data):
            ax.annotate(txt, xy=(size_data[i], error_data[i]), xytext=(20, 0), textcoords='offset points')
        plt.title("Tamanho X Erro")
        plt.xlabel("Tamanho da matriz de paridade")
        plt.ylabel("Erro pencentual de bits após correção")
        plt.show()
        return None


Gerador.variable_length(["1x1", "2x2", "3x3", "4x4"], [0.24, 0.86, 1.71, 2.52])
