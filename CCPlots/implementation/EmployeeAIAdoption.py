import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path

# Colour scheme using consistent Bitroot palette shades
BAR_C = [
        BITROOT_PALETTE["primary"],
        BITROOT_PALETTE["primary_light"],
        BITROOT_PALETTE["primary_soft"],
        BITROOT_PALETTE["secondary_light"],
    ]

class EmployeeAIAdoption(PlotExample):

    def main(self):
        # Data for the bar chart
        categories = ['Tijd bespaard', 'Focus verbeterd', 'Creativiteit verhoogd', 'Meer werkplezier']
        values = [90, 85, 84, 83]

        # Create the bar chart
        plt.figure(figsize=(10, 5), facecolor=BITROOT_PALETTE["background"])
        ax = plt.gca()
        ax.set_facecolor(BITROOT_PALETTE["background"])
        plt.bar(categories, values, color=BAR_C)
        plt.title('Impact van AI op werkervaring (% van de medewerkers eens)', color=BITROOT_PALETTE["text"])
        plt.ylabel('Percentage', color=BITROOT_PALETTE["text"])
        plt.ylim(0, 100)
        apply_bitroot_style(ax)
        plt.savefig(output_path('employee_ai_adoption.png'))

if __name__ == '__main__':
    EmployeeAIAdoption().main()