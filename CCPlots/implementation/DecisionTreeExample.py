import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, darken_color, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Decision Tree on Iris Dataset",
    },
    "nl": {
        "title": "Beslissingsboom op Iris-dataset",
    },
}


def _blend_toward(color: tuple, target: tuple, amount: float) -> tuple:
    """Linearly blend color toward target by amount (0 = full color, 1 = full target)."""
    return tuple(c + amount * (t - c) for c, t in zip(color, target))


# Class background colours — deepened just enough that white text passes
# 4.5:1 on cyan/purple; green uses the original value with dark text.
IRIS_BG = [
    to_rgba(darken_color(BITROOT_PALETTE['primary'], 0.75)),     # setosa — white text
    to_rgba(darken_color(BITROOT_PALETTE['secondary'], 0.75)),   # versicolor — white text
    to_rgba(BITROOT_PALETTE['tertiary']),                        # virginica — dark text
]
IRIS_TEXT = [
    (1.0, 1.0, 1.0, 1.0),                     # white on cyan
    (1.0, 1.0, 1.0, 1.0),                     # white on purple
    to_rgba(BITROOT_PALETTE['text']),          # dark on green
]


def _recolor_tree(ax, clf):
    """Recolor node bboxes with darkened Bitroot palette colours and white text."""
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
            face_color = to_rgba(BITROOT_PALETTE['background'])
            text_color = to_rgba(BITROOT_PALETTE['text'])
        else:
            majority_class = int(np.argmax(dist))
            purity = float(dist[majority_class]) / total
            base_rgba = IRIS_BG[majority_class]
            text_color = IRIS_TEXT[majority_class]
            # Lighten impure nodes by blending toward white (for dark bg)
            # or toward the surface background (for light bg on green)
            blend_target = (1.0, 1.0, 1.0, 1.0) if majority_class != 2 else to_rgba(BITROOT_PALETTE['background'])
            face_color = _blend_toward(base_rgba, blend_target, (1.0 - purity) * 0.25)

        bb.set_facecolor(face_color)
        bb.set_edgecolor(BITROOT_PALETTE['text'])
        bb.set_linewidth(1.5)
        bb.set_boxstyle('round,pad=0.3')

        text.set_color(text_color)
        text.set_fontsize(10)

    arrow_texts = [t for t in ax.texts if t.get_bbox_patch() is None]
    for t in arrow_texts:
        t.set_color(BITROOT_PALETTE['text'])
        t.set_fontsize(9)
        t.set_fontweight('bold')


class DecisionTreeExample(PlotExample):

    def main(self):
        iris = load_iris()
        X, y = iris.data, iris.target

        clf = DecisionTreeClassifier(max_depth=3, random_state=42)
        clf = clf.fit(X, y)

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"decision_tree_iris{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(12, 8), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            tree.plot_tree(clf, filled=False, feature_names=iris.feature_names,
                           class_names=iris.target_names, ax=ax,
                           node_ids=False, proportion=False,
                           rounded=True, precision=2)

            _recolor_tree(ax, clf)

            ax.set_title(labels["title"], color=BITROOT_PALETTE['text'],
                         fontsize=14, fontweight='bold')
            apply_bitroot_style(ax)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)
