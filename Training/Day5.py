import cv2
import numpy as np


def detect_missing_slice(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Perform edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and get the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contour = contours[0]

    # Fit an ellipse to the largest contour
    ellipse = cv2.fitEllipse(largest_contour)

    # Draw the detected contour and the fitted ellipse on the original image
    output = image.copy()
    cv2.drawContours(output, [largest_contour], -1, (0, 255, 0), 2)
    cv2.ellipse(output, ellipse, (255, 0, 0), 2)

    # Create a mask with the fitted ellipse
    ellipse_mask = np.zeros_like(gray)
    cv2.ellipse(ellipse_mask, ellipse, 255, thickness=-1)

    # Calculate the area of the largest contour and the area of the ellipse mask
    contour_area = cv2.contourArea(largest_contour)
    ellipse_area = np.sum(ellipse_mask // 255)

    # Calculate the difference between the contour area and the ellipse area
    area_difference = abs(contour_area - ellipse_area)
    area_difference_threshold = 0.05 * ellipse_area  # 5% of the ellipse area

    if area_difference > area_difference_threshold:
        print("A slice is missing.")
    else:
        print("The disc is intact.")

    # Display the result
    cv2.imshow('Detected Contour and Fitted Ellipse', output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Path to your image
image_path = 'disc_ok.jpg'
detect_missing_slice(image_path)
