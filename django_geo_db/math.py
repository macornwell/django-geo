
class Translations:

    @staticmethod
    def linear_proportion_on_y(x1, y1, x2):
        """
        x1 / y1 = x2 / (y2)
        Finding y2.
        :param x1:
        :param y1:
        :param x2:
        :return:
        """
        return y1 * x2 / x1


    @staticmethod
    def linear_proportion_on_x(x1, y1, y2):
        """
        x1 / y1 = (x2) / y2
        Finding x2.
        :param x1:
        :param y1:
        :param y2:
        :return:
        """
        return x1 * y2 / y1

    @staticmethod
    def rectangle_reduction(big_x, big_y, percentage):
        """
        Reduces the size of a rectangle by a percentage
        :param big_x:
        :param big_y:
        :param to_change_x:
        :param to_change_y:
        :param percentage: .05 = (5%)
        :return:
        """
        changed_x = int(big_x * percentage)
        changed_y = int(Translations.linear_proportion_on_y(big_x, big_y, changed_x))
        return changed_x, changed_y

