import collections

NUM_TOKENS_OF_EACH_COLOUR = 10
ROBOT_MULTIPLIER = 3


class InvalidScoresheetException(Exception):
    pass


class Scorer(object):
    # Note: if the arena colours (from arena.yaml) change,
    # both this and the printed score-sheets will need to change
    ZONE_COLOURS = [
        'G',    # zone 0 = green
        'O',    # zone 1 = orange
        'P',    # zone 2 = purple
        'Y',    # zone 3 = yellow
    ]

    ZONE_SCORE_MAP = [
        [ 2,  2,  2,  2,  2],
        [ 2,  7,  7,  7,  2],
        [ 2,  7, 30,  7,  2],
        [ 2,  7,  7,  7,  2],
        [ 2,  2,  2,  2,  2],
    ]

    def __init__(self, teams_data, arena_data):
        self._teams_data = teams_data
        self._zone_contents = arena_data['other']['zone_contents']

        for row in self._zone_contents:
            for zone in row:
                zone['tokens'] = collections.Counter(
                    zone['tokens'].replace(' ', ''),
                )

        self._colour_to_team = {
            self.ZONE_COLOURS[info['zone']]: tla
            for tla, info in self._teams_data.items()
        }

    def validate(self, extra):
        if len(self._zone_contents) != 5:
            raise InvalidScoresheetException(
                "Wrong number of rows: {} != 5".format(len(self._zone_contents)),
            )

        tokens = collections.Counter()
        robots = collections.Counter()
        for idx, row in enumerate(self._zone_contents):
            if len(row) != 5:
                raise InvalidScoresheetException(
                    "Wrong number of zones in row {}: {} != 5".format(idx, len(row)),
                )

            for zone in row:
                robots.update(zone['robots'])
                tokens.update(zone['tokens'])

        extra_robots = set(robots.keys()) - set(self._teams_data.keys())
        if extra_robots:
            raise InvalidScoresheetException(
                "Unepxected robot(s): {!r}".format(extra_robots),
            )

        for robot, count in robots.items():
            if count > 1:
                raise InvalidScoresheetException(
                    "{} appears {} times! (can only appear at most once)".format(
                        robot,
                        count,
                    ),
                )

        extra_token_colours = set(tokens.keys()) - set(self.ZONE_COLOURS)
        if extra_token_colours:
            raise InvalidScoresheetException(
                "Unepxected token colour(s): {!r}".format(extra_token_colours),
            )

        for colour, count in tokens.items():
            if count > NUM_TOKENS_OF_EACH_COLOUR:
                raise InvalidScoresheetException(
                    "Too many {} tokens ({} > {})".format(
                        colour,
                        count,
                        NUM_TOKENS_OF_EACH_COLOUR,
                    ),
                )

    def _compute_zone_points(self, zone_token_counts, score):
        if len(zone_token_counts) == 1:
            colour, = zone_token_counts.keys()
            return colour, score

        if len(zone_token_counts) > 1:
            # check for a tie
            (colour, count_1), (_, count_2) = zone_token_counts.most_common(2)
            if count_1 != count_2:
                return colour, score

        # either a tie or no tokens
        return None, 0

    def multipler_indices(self, row, col):
        if 0 < row:
            yield row - 1, col

        if 0 < col:
            yield row, col - 1

        yield row, col

        if col < 4:
            yield row, col + 1

        if row < 4:
            yield row + 1, col

    def calculate_scores(self):
        # Build an understanding of who owns which zones and how much the zones
        # are worth. This ends up with each zone being (Optional[Colour], int)
        zone_points = [
            [
                self._compute_zone_points(zone['tokens'], score)
                for zone, score in zip(*row)
            ]
            for row in zip(self._zone_contents, self.ZONE_SCORE_MAP)
        ]

        def apply_multiplier(row, col, num_robots):
            # nonlocal zone_points

            # Apply the 3 times multiplier for robots being in a given zone,
            # which applies to that zone and its cardinal direction zones.
            score_multiplier = ROBOT_MULTIPLIER ** num_robots
            for i, j in self.multipler_indices(row, col):
                (owner, score) = zone_points[i][j]
                zone_points[i][j] = (owner, score * score_multiplier)

        # now add the robot multipliers
        for i, row in enumerate(self._zone_contents):
            for j, zone in enumerate(row):
                num_robots = len(zone['robots'])
                if num_robots:
                    apply_multiplier(i, j, num_robots)

        scores = {tla: 0 for tla in self._teams_data.keys()}
        for row in zone_points:
            for colour, score in row:
                if colour is not None:
                    scores[self._colour_to_team[colour]] += score

        return scores


if __name__ == '__main__':
    import libproton
    libproton.main(Scorer)
