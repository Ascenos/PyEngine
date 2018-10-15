from engine import *



class Terrain(RigidObject):
    def _base(self):
        # Generate base terain
        start = 0.1 * self.__width
        end = 0.9 * self.__width
        # Points from which a polynom is generated.
        x_points = np.linspace(int(start), int(end) - 1, 11)
        # Static polynom y values, to be multiplied by height
        statics = [0, 0.2, 0.22, 0.26, 0.28, 0.24, 0.20, 0.22, 0.26, 0.2, 0]
        # Generate actual points from static values
        y_points = np.asarray([number * self.__height for number in statics])
        # Compute actual ponynomial values
        x_values = np.arange(0, self.__width, 1, dtype = np.int16)
        y_values = legendre_polynom(x_points, y_points)(x_values)
        # Mask for values outside of the polynom
        np.putmask(y_values, np.logical_or(x_values < start, x_values > end), 0)
        # Set terrain to the values
        self._terain = y_values.astype(dtype = np.int32)

    def generate_impact(self, x, size):
        """
        Generates impact on terrain at position x with depth size and width
        dependent on the impact-width-factor.

        Input:
            x    : int
            size : int

        Returns:
            None
        """
        size_factor = self._IMPACT_WIDTH_FACTOR * size
        # Range of the Impact for x - size_factor to x + size_factor.
        temp_range = np.arange(1, size_factor * 2, 1, dtype = np.float64)
        # Cosinus values for impact ~0 at borders and ~-2 at the center.
        temp_cos = np.cos(temp_range / size / self._IMPACT_WIDTH_FACTOR * np.pi)
        # Cosinus values multiplied by the factor for actual impact depth.
        impact = ((temp_cos - 1) * size / 2).astype(dtype = np.int32)

        # Avoid trying to write outside the terrain array.
        start = max(x - size_factor + 1, 0)
        end = min(x + size_factor, self.__width)
        #self.impact.append([start, end])
        self._terrain[start:end] += impact

    def relative_terrain(self, size):
        """
        Return the amount of terrain values needed to be compressed in order
        to obtain the wanted amount of pixels.
        """
        terrain = np.zeros(size[0], dtype = np.int32)
        size_factor = self.__width // size[0]
        for i in range(size_factor):
            terrain += self.terrain[np.arange(i, self.__width, size_factor)]
        return terrain // size_factor ** 2

    def collision_info(self, point):
        # TODO calculate point collision
        pass

    def render(self, frame):
        # TODO move function from old gui into here
        pass