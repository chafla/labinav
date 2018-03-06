"""
Very nasty and unoptimized code for detecting largest contours. Mostly drawn from a couple tutorials.

Written 11/2/17
"""

import cv2
import numpy as np


FIND_LARGEST_EXTERNAL = True


def get_inner_contours(cnts, hierarchy):

    inner_contours = []
    new_hierarchy = []

    if len(cnts) == 0:
        return [], []

    for i, cont in enumerate(cnts):
        if hierarchy[0][i][2] == -1 and cv2.contourArea(cont) > 200:  # No child in the hierarchy -- no holes
            inner_contours.append(cont)
            new_hierarchy.append(hierarchy[0][i])

    if len(inner_contours) > 0:

        inner_contours, new_hierarchy = zip(*sorted(zip(inner_contours, new_hierarchy), key=lambda c: cv2.contourArea(c[0]), reverse=True)[:10])  # Sort the combined

    return inner_contours, new_hierarchy


def sort_contours(cnts, method="left-to-right"):
    if len(cnts) == 0:
        return [], []
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return cnts, boundingBoxes


def draw_contour(image, c, i):
    # compute the center of the contour area and draw a circle
    # representing the center
    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # cv2.fillPoly(image, pts=[c], color=(i % 255, 255, 255))

        # draw the countour number on the image
        cv2.putText(image, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (255, 255, 255), 2)

        # return the image with the contour number drawn on it
    return image


camera = cv2.VideoCapture(0)
# originally -6
camera.set(cv2.CAP_PROP_EXPOSURE, -4)  # Set exposure as low as possible

try:
    # Camera settings
    while True:

        ret, frame = camera.read()

        # Creating an empty array to fill with edges
        accumEdged = np.zeros(frame.shape[:2], dtype="uint8")

        # loop over the blue, green, and red channels, respectively
        for chan in cv2.split(frame):
            # blur the channel, extract edges from it, and accumulate the set
            # of edges for the image
            chan = cv2.medianBlur(chan, 11)  # Blur to make things easier to use
            # cv2.imshow("blur", chan)
            edged = cv2.Canny(chan, 50, 200)  # Do the edge detection
            accumEdged = cv2.bitwise_or(accumEdged, edged)  # By oring, we "add" new edges to the array

            # Step 2

        (_, cnts, hierarchy) = cv2.findContours(accumEdged.copy(), cv2.RETR_CCOMP,
                                     cv2.CHAIN_APPROX_SIMPLE)
        cnts, hierarchy = get_inner_contours(cnts, hierarchy)
        # Would use sorted but we run into issues

        # c = [c for c in cnts if cv2.isContourConvex(c)]  # Only keep the complex contours

        orig = frame.copy()

        for (i, c) in enumerate(cnts):
            orig = draw_contour(orig, c, i)

        # show the original, unsorted contour image
        # cv2.imshow("Unsorted", orig)

        # sort the contours according to the provided method
        (cnts, boundingBoxes) = sort_contours(cnts, method="top-to-bottom")

        # loop over the (now sorted) contours and draw them
        for (i, c) in enumerate(cnts):
            draw_contour(frame, c, i)
            x, y, w, h = boundingBoxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.fillPoly(frame, [c], (255, 0, 0))

            # box = cv2.boxPoints(boundingBoxes[i])
            # box = np.int0(box)
            # if len([boundingBoxes[i]]) > 0:
            #     cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

        # show the accumulated edge map
        cv2.imshow("Edge Map", accumEdged)

        cv2.imshow("base", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()
