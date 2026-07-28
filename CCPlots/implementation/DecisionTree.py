"""
Decision tree (max depth 3) trained on the Iris dataset with node boxes
recoloured using the Bitroot palette. Impure nodes are lightened
proportionally to their impurity.

Figures
-------
- ``decision_tree_iris.png`` / ``_NL.png`` — tree plot

Configuration
-------------
``CCPlots/plot_configs/decision_tree.json``
"""
import numpy as np
from matplotlib.colors import to_rgba
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from CCPlots.PlotExample import PlotExample
from CCPlots.config import GLOBAL_RANDOM_STATE


def _blend_toward(color: tuple, target: tuple, amount: float) -> tuple:
    return tuple(c + amount * (t - c) for c, t in zip(color, target))


class DecisionTree(PlotExample):

    CONFIG_KEY = "decision_tree"

    def _node_bg_colors(self):
        """Return (bg_rgba_list, text_rgba_list) for the three Iris classes."""
        setosa = to_rgba(self.resolve_color('node_setosa'))
        versicolor = to_rgba(self.resolve_color('node_versicolor'))
        virginica = to_rgba(self.resolve_color('node_virginica'))
        bg = [setosa, versicolor, virginica]
        white = (1.0, 1.0, 1.0, 1.0)
        dark = to_rgba(self.text_color)
        text = [white, white, dark]
        return bg, text

    def _recolor_tree(self, ax, clf):
        """Recolor node bboxes using config-driven colours."""
        iris_bg, iris_text = self._node_bg_colors()
        bg_fallback = to_rgba(self.resolve_color('node_empty_bg'))

        children_left = clf.tree_.children_left
        children_right = clf.tree_.children_right
        values = clf.tree_.value

        bbox_texts = [t for t in ax.texts if t.get_bbox_patch() is not None]

        node_order = []
        stack = [0]
        while stack:
            node_id = stack.pop()
            node_order.append(node_id)
            right = children_right[node_id]
            if right != -1:
                stack.append(right)
                stack.append(children_left[node_id])

        for node_id, text in zip(node_order, bbox_texts):
            bb = text.get_bbox_patch()
            dist = values[node_id, 0, :]
            total = float(dist.sum())
            if total == 0:
                face_color = bg_fallback
                text_color = to_rgba(self.text_color)
            else:
                majority_class = int(np.argmax(dist))
                purity = float(dist[majority_class]) / total
                base_rgba = iris_bg[majority_class]
                text_color = iris_text[majority_class]
                blend_target = (1.0, 1.0, 1.0, 1.0) if majority_class != 2 else bg_fallback
                face_color = _blend_toward(base_rgba, blend_target, (1.0 - purity) * 0.25)

            bb.set_facecolor(face_color)
            bb.set_edgecolor(to_rgba(self.resolve_color('node_edge')))
            bb.set_linewidth(1.5)
            bb.set_boxstyle('round,pad=0.3')

            text.set_color(text_color)
            text.set_fontsize(10)

        arrow_color = to_rgba(self.resolve_color('arrow_text'))
        for t in (t for t in ax.texts if t.get_bbox_patch() is None):
            t.set_color(arrow_color)
            t.set_fontsize(9)
            t.set_fontweight('bold')

    def main(self):
        iris = load_iris()
        X, y = iris.data, iris.target

        clf = DecisionTreeClassifier(max_depth=3, random_state=GLOBAL_RANDOM_STATE)
        clf = clf.fit(X, y)

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            tree.plot_tree(clf, filled=False, feature_names=iris.feature_names,
                           class_names=iris.target_names, ax=ax,
                           node_ids=False, proportion=False,
                           rounded=True, precision=2)

            self._recolor_tree(ax, clf)

            ax.set_title(labels["title"], color=self.text_color,
                         fontsize=14, fontweight='bold')
            self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)
