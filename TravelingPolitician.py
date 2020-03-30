import multiprocessing
from functools import partial
import pandas
import selenium
from selenium import webdriver
import geopy.distance
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from itertools import permutations
import os


def get_zip_code(state_name):
    """Returns zip code of the state capital

    :param state_name: Name of state
    :type state_name: str
    :return: Zip Code of state capital
    :rtype: int
    """
    url = "https://google.com"
    this_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(this_dir, 'chromedriver.exe')
    path_to_chromedriver = file_path  # Path to access a chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(path_to_chromedriver, options=chrome_options)
    browser.get(url)
    try:
        # Search for Capital
        wait = WebDriverWait(browser, 10)
        wait.until(ec.presence_of_element_located((By.NAME, 'q')))
        search = browser.find_element_by_name('q')
        search.send_keys("Capital of " + state_name + " State")
        search.send_keys(Keys.RETURN)
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'FLP8od')))
        capital = browser.find_element_by_class_name('FLP8od').text
        # Search for Zip
        browser.get(url)
        wait.until(ec.presence_of_element_located((By.NAME, 'q')))
        search = browser.find_element_by_name('q')
        search.send_keys(capital + " Zip Code")
        search.send_keys(Keys.RETURN)
        wait.until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'TZNJBf')))
        zip_code = browser.find_element_by_class_name('TZNJBf')
        return int(zip_code.text)
    except selenium.common.exceptions.TimeoutException:
        browser.quit()
        print("Error")
        return "101"


this_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(this_dir, 'zip-codes-database-FREE.csv')
data_frame = pandas.read_csv(file_path)


def get_location(zip_code):
    """Returns the latitude and longitude of a zip code

    :param zip_code: Zip Code of Location
    :type zip_code: int
    :return: Coordinates of location
    :rtype: tuple of latitude, longitude
    """
    df = data_frame[data_frame['ZipCode'] == zip_code]
    return df['Latitude'].values, df['Longitude'].values


washington_dc_zip_code = 20001


def compute_path_distance(path, coordinates):
    """Returns the distance to traverse the path from start to finish

    :param path: The state names in order
    :type path: list of string
    :param coordinates: A dictionary of state names to coordinates
    :type coordinates: dict of string to tuple
    :return: The distance
    :rtype: numeric value
    """
    d = 0
    previous_coords = None
    for x in path:
        coords = coordinates[x]
        if previous_coords is not None:
            d += geopy.distance.distance(previous_coords, coords).miles
        previous_coords = coords
    return d


def generate_paths(start, middles, end):
    """Generates all possible permutations of paths

    :param start: Name of first state
    :type start: str
    :param middles: Middle state names
    :type middles: list of str
    :param end: Final state
    :type end: str
    :return: All permutations of paths
    :rtype: list of list of string
    """
    paths = []
    perms = list(permutations(middles))
    for perm in perms:
        ap = [start]
        for x in perm:
            ap.append(x)
        ap.append(end)
        paths.append(ap)
    return paths


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
    path = ""
    coordinates = {}
    for x in [start, end]:
        zip_code = washington_dc_zip_code if x == 'Washington D.C.' else get_zip_code(x)
        location = get_location(zip_code)
        coordinates[x] = location
    for x in middles:
        zip_code = washington_dc_zip_code if x == 'Washington D.C.' else get_zip_code(x)
        location = get_location(zip_code)
        coordinates[x] = location
    paths = generate_paths(start, middles, end)
    pool = multiprocessing.Pool()
    partial_paths = partial(compute_path_distance, coordinates=coordinates)
    lengths = pool.map(partial_paths, paths)
    smallest_distance = lengths[0]
    smallest_path = paths[0]
    for x in range(len(lengths)):
        if float(smallest_distance) > float(lengths[x]):
            smallest_distance = lengths[x]
            smallest_path = paths[x]

    for n in smallest_path:
        path += n + "->"
    path = path[0: -2]
    return smallest_distance, path


if __name__ == '__main__':
    start = input("Starting State: ")
    middle = input("Comma Delimited Middle States: ")
    end = input("End State: ")
    middle_arr = middle.split(",")
    print(traveling_politician_n(start, middle_arr, end))
