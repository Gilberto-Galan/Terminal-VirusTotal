
import matplotlib.pyplot as plt
import os


def plot_results(positives, negatives, export_image=False, image_filename="results_plot.png"):
    labels = ['Detectado', 'No detectado']
    values = [positives, negatives]

    plt.bar(labels, values, color=['red', 'green'])
    plt.title('Resultados del Escaneo')
    plt.xlabel('Resultado')
    plt.ylabel('Cantidad de Motores Antivirus')

    if export_image:
        ruta_guardado = os.path.join('Gráficas', 'grafica.png')
        plt.savefig(ruta_guardado)
        print(f"Gráfica guardada como {image_filename}")
    else:
        plt.show()






