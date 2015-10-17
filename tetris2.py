#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

# wall, elements are global variables

# createBorder(element)

# isValid = isPositionValid(element, i, j)

# score = getBorderScore(element, i, j)

# getBestPosition(element)
# listOfNewAttachmentPoints = placeElement(element, i, j)

def parse(filename):
	return 10, 10, []

def remove_trivial_elements(elements):
	return [], elements

def create_border(elements):
	pass

def get_best_position(element, wall):
	return false

def sort_by_score(elements):
	return elements

def place_best_element(elements, placedElements, wall):
	if len(elements) == 0:
		return elements, placedElements, wall
	else:
		wall = place_element(wall, elements[0])
		placedElements.append(elements[0])
		return elements[1:], placedElements, wall

def place_element(wall, element):
	return wall

def place_trivial_elements(trivialElements, placedElements, wall):
	return wall, placedElements

def fill(n, m, wall, elements):
	trivialElements, elements = remove_trivial_elements(elements)
	placedElements = []
	create_border(elements)
	while len(elements) > 0:
		newElements = []
		for element in elements:
			if (get_best_position(element, wall)):
				newElements.append(element)
		sort_by_score(newElements)
		newElements, placedElements, wall = place_best_element(newElements, placedElements, wall)
		elements = newElements
	wall, placedElements = place_trivial_elements(trivialElements, placedElements, wall)
	return wall, placedElements

def export_result(filename, placedElements):
	pass

if __name__ == "__main__":
	n, m, elements = parse("tetris.txt")
	wall = np.zeros((n+20,m+20), dtype=np.int)

	wall, placedElements = fill(n, m, wall, elements)
	export_result("output.txt", placedElements)