#!/usr/bin/env python

# pylint: disable=missing-module-docstring

from typing import List, NamedTuple
import os
import logging
import random
import re
import sys
import time

from numpy import ndarray
import click
import cv2 as cv
import numpy as np
import pyautogui
from PIL import Image, ImageOps


# These define the main function that runs the autoclicker
@click.command()
@click.option('--sleep_max', default=5.)
@click.option('--sleep_min', default=0.)
# Main function that runs the autoclicker.
# Args:
#    sleep_max (float): Maximum sleep time between auto clicks.
#    sleep_min (float): Minimum sleep time between auto clicks.
def run(sleep_max: float, sleep_min: float) -> None:  # pylint: disable=missing-function-docstring

    # Configure logging settings
    logging.basicConfig(
        datefmt='%m/%d/%Y %I:%M:%S %p',
        format='%(asctime)s [%(levelname)s] %(message)s',
        level=logging.INFO,
    )
    templates = _get_templates()  # Get the list of template images
    # Run the autoclicker in a loop
    while True:
        # Generate a random sleep time
        sleep_seconds = random.uniform(sleep_min, sleep_max)
        logging.info('Sleeping for %f seconds', sleep_seconds)
        time.sleep(sleep_seconds)
        try:
            _find_and_click(templates)
        except cv.error:  # pylint: disable=no-member
            logging.info('Ignoring OpenCV error')


# used to store information about a specific template image
class _Template(NamedTuple):
    array: ndarray
    name: str
    threshold: int


# Define the main function to find and click on templates
# Find and click on matching templates in the screenshot.
def _find_and_click(templates: List[_Template]) -> None:
    screenshot_image = pyautogui.screenshot()
    screenshot = _image_to_grayscale_array(screenshot_image)
    for template in templates:
        # SIFT patent expired in 2015, so it has been moved to the main OpenCV repository.
        # "pip install opencv-python" only.
        sift = cv.SIFT.create()  # pylint: disable=no-member
        _, template_descriptors = sift.detectAndCompute(template.array, mask=None)
        screenshot_keypoints, screenshot_descriptors = sift.detectAndCompute(screenshot, mask=None)
        matcher = cv.BFMatcher()  # pylint: disable=no-member
        matches = matcher.knnMatch(template_descriptors, screenshot_descriptors, k=2)
        points = np.array([screenshot_keypoints[m.trainIdx].pt for m, _ in matches if m.distance < template.threshold])
        if points.shape[0] == 0:
            continue
        point = np.median(points, axis=0)
        current_mouse_pos = pyautogui.position()
        logging.info('Saving current mouse position at x=%f y=%f', *current_mouse_pos)
        pyautogui.click(*point)
        logging.info('Clicking on %s at coordinates x=%f y=%f', template.name, *point)
        pyautogui.moveTo(*current_mouse_pos)
        return
    logging.info('No matches found')


# This responsible for retrieving and preparing template images that will be used for image matching within the Nexus AutoDL script.
# basically retrieve a list of template images from the templates directory.
def _get_templates() -> List[_Template]:  # pylint: disable=too-many-locals
    templates: List[_Template] = []  # Add the type annotation here
    try:
        root_dir = sys._MEIPASS  # type: ignore  # pylint: disable=no-member,protected-access
    except AttributeError:
        root_dir = '.'
    templates_dir = os.path.join(root_dir, 'templates')
    pattern = re.compile(r'^([1-9][0-9]*)_([1-9][0-9]*)_(.+)\.png$')
    basenames = os.listdir(templates_dir)
    matches = (pattern.match(basename) for basename in basenames)
    filtered_matches = (match for match in matches if match is not None)
    groups = (match.groups() for match in filtered_matches)
    sorted_groups = sorted(groups, key=lambda t: int(t[0]))
    for index, threshold, name in sorted_groups:
        path = os.path.join(templates_dir, f'{index}_{threshold}_{name}.png')
        image = Image.open(path)
        array = _image_to_grayscale_array(image)
        template = _Template(array=array, name=name, threshold=int(threshold))
        templates.append(template)
    return templates


# Convert a PIL Image to a grayscale NumPy array.
def _image_to_grayscale_array(image: Image.Image) -> ndarray:
    image = ImageOps.grayscale(image)
    array = np.array(image)
    return array


# Execute the main function only if the script is run directly
if __name__ == '__main__':
    run()  # pylint: disable=no-value-for-parameter
