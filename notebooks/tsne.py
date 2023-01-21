from mowl.visualization import TSNE as MTSNE
from sklearn.manifold import TSNE as SKTSNE
import numpy as np
import matplotlib.pyplot as plt

class TSNE(MTSNE):

    def __init__(self, *args, perplexity=5, thickness = 50,  **kwargs):
        super().__init__(*args, **kwargs)

        self.perplexity = perplexity
        self.thickness = thickness

    def generate_points(self, epochs, workers=1, verbose=0):
        """This method will call the :meth:`sklearn.manifold.TSNE.fit_transform`
        method to generate the points for the plot.

        :param epochs: Number of epochs to run the TSNE algorithm
        :type epochs: int
        :param workers: Number of workers to use for parallel processing. Defaults to 1.
        :type workers: int, optional
        :param verbose: Verbosity level. Defaults to 0.
        """
        points = np.array(list(self.embeddings.values()))
        if np.iscomplexobj(points):
            if verbose:
                warnings.warn("Complex numpy array detected. Only real part will be considered",
                              UserWarning)
            points = points.real
        self.points = SKTSNE(n_components=2, verbose=verbose, n_iter=epochs, n_jobs=workers, perplexity=self.perplexity)
        self.points = self.points.fit_transform(points)
        self.plot_data = {}

        for name, idx in self.embedding_idx_dict.items():
            label = self.labels[name]
            x, y = tuple(self.points[idx])

            if label not in self.plot_data:
                self.plot_data[label] = [], []
            self.plot_data[label][0].append(x)
            self.plot_data[label][1].append(y)

    def show(self, thickness = None):
        """ This method will call the :meth:`matplotlib.pyplot.show` method to show the plot.
        """
        if thickness is None:
            thickness = self.thickness
            
        fig, ax = plt.subplots(figsize=(15, 15))

        for label, (xs, ys) in self.plot_data.items():
            color = self.class_color_dict[label]
            ax.scatter(xs, ys, color=color, label=label, s=thickness)
            ax.text(xs[0]+0.5, ys[0]+0.5, label, fontsize=12)

            ax.legend()
            ax.grid(True)

        plt.show()
