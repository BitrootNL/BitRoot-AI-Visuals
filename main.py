"""
main.py

Run all examples from the CCPlots library to make my life a little easier.

Please note that the entire configuration for the plots is in CCPlots (config.py),
including the output folder.
"""
import CCPlots


def all_plots():
    """
    This function will run all the PlotExample implementations to regenerate plots.

    This is a slow process and will give you lots of warnings (thanks dummy data and ChatGPT)
    :return:
    """
    # Retrieve all implementations of examples
    classes = [
        cls for name, cls in CCPlots.__dict__.items()
        if isinstance(cls, type)
           and cls.__module__.startswith('CCPlots.implementation')
    ]

    # Run all examples
    for cls in classes: instance = cls().main()

if __name__ == "__main__":
    # This takes a while, comment out at your own risk
    all_plots()