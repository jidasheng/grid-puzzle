import random

class Model:
    def __init__(self):
        self.groups = self._build_possible_groups()

    def _build_possible_groups(self):
        groups = []
        self._build_lines(groups)
        self._build_rectangles(groups)
        self._build_rhombus(groups)
        return groups

    @staticmethod
    def _build_lines(groups):
        # horizontal
        for row in range(4):
            groups.append([(row, col) for col in range(4)])

        # vertical
        for col in range(4):
            groups.append([(row, col) for row in range(4)])

        # cross
        groups.append([(i, i) for i in range(4)])
        groups.append([(i, 3 - i) for i in range(4)])

    @staticmethod
    def _build_rectangles(groups):
        for offset_row in range(3):
            for offset_col in range(3):
                groups.append([(r + offset_row, c + offset_col) for r in range(2) for c in range(2)])

    @staticmethod
    def _build_rhombus(groups):
        for center_row in range(1, 3):
            for center_col in range(1, 3):
                groups.append([
                    (center_row + o_row, center_col + o_col)
                    for o_row, o_col in [(-1, 0), (1, 0), (0, 1), (0, -1)]
                ])

    def random_group(self):
        return random.choice(self.groups)

    def probabilities(self, true_obs=(), false_obs=()):
        """calculate the probabilities of all cells

        :param true_obs: a list of tuples, eg: [(0, 0), (3, 2)]
        :param false_obs: a list of tuples, eg: [(0, 0), (3, 2)]
        :return: a 4x4 array
        """
        valid_shapes = self.groups[:]
        for o in true_obs:
            valid_shapes = [s for s in valid_shapes if o in s]
        for o in false_obs:
            valid_shapes = [s for s in valid_shapes if o not in s]

        total_count = len(valid_shapes)
        probs = []
        for row in range(4):
            row_probs = []
            for col in range(4):
                pos = (row, col)
                num = sum([1 for s in valid_shapes if pos in s])
                prob = num / total_count
                row_probs.append(prob)
            probs.append(row_probs)
        return probs

    @staticmethod
    def print_probs(probs, observations=()):
        print("{0} probs {0}".format("-"*15))
        for row, row_probs in enumerate(probs):
            for col, prob in enumerate(row_probs):
                print("{:>8}".format("x") if (row, col) in observations else "{:8.3f}".format(prob), end="")
            print("")


def test():
    model = Model()
    probs = model.probabilities()
    model.print_probs(probs)

    observations = [(1, 1)]
    probs = model.probabilities(observations)
    model.print_probs(probs, observations)

    observations = [(1, 1), (2, 2)]
    probs = model.probabilities(observations)
    model.print_probs(probs, observations)

    observations = [(1, 1), (2, 2), (2, 0)]
    probs = model.probabilities(observations)
    model.print_probs(probs, observations)


if __name__ == '__main__':
    test()
