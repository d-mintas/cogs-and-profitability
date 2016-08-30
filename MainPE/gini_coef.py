def GRLC(values):
    '''
    Calculate Gini index, Gini coefficient, Robin Hood index, and points of
    Lorenz curve values as given as lists of x & y points [[x1, x2], [y1, y2]]
    @param values: List of values
    @return: [Gini coefficient, Robin Hood index] 
    '''
    n = len(values)
    assert(n > 0), 'Empty list of values'
    sortedValues = sorted(values)  # Sort smallest to largest

    # Find cumulative totals
    cumv = [0]
    for i in range(n):
        cumv.append(sum(sortedValues[0:(i + 1)]))

    # Calculate Lorenz points
    LorenzPoints = [[], []]
    sumYs = 0  # Some of all y values
    robinHoodIdx = -1  # Robin Hood index max(x_i, y_i)
    for i in range(1, n + 2):
        x = 100.0 * (i - 1) / n
        y = 100.0 * (cumv[i - 1] / float(cumv[n]))
        LorenzPoints[0].append(x)
        LorenzPoints[1].append(y)
        sumYs += y
        maxX_Y = x - y
        if maxX_Y > robinHoodIdx:
            robinHoodIdx = maxX_Y

    giniIdx = 100 + (100 - 2 * sumYs) / n  # Gini index

    return [giniIdx / 100, robinHoodIdx]

if __name__ == "__main__":
    # Example
    sample = [1, 6]

    result = GRLC(sample)

    print('Gini Coefficient:', result[0])
    print('Robin Hood Index:', result[1])
