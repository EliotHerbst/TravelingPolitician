import itertools
import os
import sys
import json
import geopy.distance
import pandas

zip_code = {
    'Alabama': 36043,
    'Alaska': 99801,
    'Arizona': 85001,
    "Arkansas": 72201,
    "California": 94203,
    "Colorado": 80201,
    "Connecticut": 6101,
    "Delaware": 19901,
    "Florida": 32301,
    "Georgia": 30301,
    "Hawaii": 96801,
    "Idaho": 83701,
    "Illinois": 62701,
    "Indiana": 46201,
    "Iowa": 50301,
    "Kansas": 66601,
    "Kentucky": 40601,
    "Louisiana": 70801,
    "Maine": 4330,
    "Maryland": 21401,
    "Massachusetts": 2108,
    "Michigan": 48901,
    "Minnesota": 55101,
    "Mississippi": 39201,
    "Missouri": 65101,
    "Montana": 59601,
    "Nebraska": 68501,
    "Nevada": 89701,
    "New Hampshire": 3301,
    "New Jersey": 8601,
    "New Mexico": 87501,
    "New York": 12201,
    "North Carolina": 27601,
    "North Dakota": 58501,
    "Ohio": 43201,
    "Oklahoma": 73101,
    "Oregon": 97301,
    "Pennsylvania": 17101,
    "Rhode Island": 2901,
    "South Carolina": 29201,
    "South Dakota": 57501,
    "Tennessee": 37201,
    "Texas": 73301,
    "Utah": 84101,
    "Vermont": 5601,
    "Virginia": 23218,
    "Washington": 98501,
    "West Virginia": 25301,
    "Wisconsin": 53701,
    "Wyoming": 82001,
    "Washington D.C.": 20500
}

this_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(this_dir, 'zip-codes-database-FREE.csv')
data_frame = pandas.read_csv(file_path)


def get_location(z):
    """Returns the latitude and longitude of a zip code

    :param z: Zip Code of Location
    :type z: int
    :return: Coordinates of location
    :rtype: tuple of latitude, longitude
    """
    df = data_frame[data_frame['ZipCode'] == z]
    return df['Latitude'].values, df['Longitude'].values


def distance_matrix(end, middles, coordinates):
    """Intenal method for creating distance matrix with dummy node

    :param end: end location
    :param middles: array of middles
    :param coordinates: dict of name to coordinate
    :return: distance matrix
    """
    mat = []
    for x in middles:
        local = []
        if x is end:
            for y in middles:
                local.append(geopy.distance.distance(coordinates[x], coordinates[y]).miles)
            local.append(float(0))
        else:
            for y in middles:
                local.append(geopy.distance.distance(coordinates[x], coordinates[y]).miles)
            local.append(float('inf'))
        mat.append(local)
    local = [float(0)]
    for i in range(len(middles) - 1):
        local.append(float('inf'))
    mat.append(local)
    return mat


def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization. Written by CarlEkerot
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2 ** n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    opt, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return opt, list(reversed(path))


def traveling_politician_n(start, middles, end):
    """Returns solution of traveling politician problem with n middle states

    :param start: starting point
    :type start: str
    :param middles: middle states
    :type middles: list of str
    :param end: final state
    :type end: str
    :return: solution for traveling politician problem
    :rtype: tuple of smallest distance, path
    """
    coordinates = {}

    middles.insert(0, start)
    middles.append(end)
    for x in middles:
        z_code = zip_code[x]
        location = get_location(z_code)
        coordinates[x] = location
    dist_mat = distance_matrix(end, middles, coordinates)
    sol = held_karp(dist_mat)
    length = sol[0]
    order = sol[1]
    name_order = []
    for x in order:
        if x < len(middles):
            name_order.append(middles[x])
    return length, name_order


if __name__ == '__main__':
    this_dir = os.path.dirname(os.path.realpath(__file__))
    log_path = os.path.join(this_dir, 'log.txt')
    log = open(log_path, 'a+')
    log.write('\n')
    data = None
    log.write('Args: ' + str(sys.argv) + ' ')
    try:
        with open(sys.argv[1]) as json_data:
            data = json.load(json_data)
        if data is None:
            print("Error: Could not read JSON")
        start = data['start']
        middle = data['middle']
        middle = middle.split(',')
        end = data['end']
        solution = traveling_politician_n(start, middle, end)
        solution_dict = {'Input': data, 'Total Distance': solution[0], 'Path': solution[1]}
        log.write('solution:' + str(solution_dict) + ' ')
        f = None
        path = sys.argv[2]
        f = open(path, 'w+')
        json.dump(solution_dict, f, indent=4)
        f.close()
    except ValueError as err:
        log.write(str(err))
    except OSError as err:
        log.write(str(err))
    except NameError as err:
        log.write(str(err))
    except TimeoutError as err:
        log.write(str(err))
    except:
        log.write("Unknown Error")
        raise
