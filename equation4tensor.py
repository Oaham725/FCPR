# @Author: Xiao-Han Xi, Hao Ma
# -*- coding = 'utf-8' -*-
# @Time:2024/11/4 12:39
# @File: matrix_process.py
# @Software: PyCharm

'''
This algorithm implements two mathematical functions for tensor calculations:
1. your_function (f1): Calculates a ratio based on trigonometric expressions involving theta and chi angles
2. another_function(f2): Another calculates the ratio based on a triangular expression involving theta and chi angles
Both functions are used to find specific angle combinations that satisfy given conditions

Usage:
    python equation4tensor.py --r1 VALUE --r2 VALUE --target1 VALUE --target2 VALUE [--tolerance VALUE]
    
    The VALUEs are from the results of matrix_process.py
    r1 = r_1, r2 = r_2; targer1=I_1=Icc/Iaa, targer2=I_2=Iac/Iaa

Example:
    python equation4tensor.py --r1 -9.52 --r2 -1.06 --target1 8.78 --target2 2.98 --tolerance 0.05
'''

import math
import argparse
import sys

def your_function(theta, chi, r1, r2):
    """
    Calculate first tensor equation ratio based on angles and r-values
    
    Args:
        theta (float): Angle theta in radians
        chi (float): Angle chi in radians
        r1 (float): First ratio parameter
        r2 (float): Second ratio parameter
    
    Returns:
        float: Ratio of two trigonometric expressions
    """
    # Calculate numerator: 4 * (sin²θ * (r₁cos²χ + r₂sin²χ) + cos²θ)²
    numerator = 4 * (
            math.sin(theta) ** 2 * (r1 * math.cos(chi) ** 2 + r2 * math.sin(chi) ** 2) +
            math.cos(theta) ** 2
    ) ** 2

    # Calculate denominator: (cos²θ * (r₁cos²χ + r₂sin²χ) + (r₁sin²χ + r₂cos²χ) + sin²θ)²
    denominator = (
                          math.cos(theta) ** 2 * (r1 * math.cos(chi) ** 2 + r2 * math.sin(chi) ** 2) +
                          (r1 * math.sin(chi) ** 2 + r2 * math.cos(chi) ** 2) +
                          math.sin(theta) ** 2
                  ) ** 2

    result = numerator / denominator
    return result

def another_function(theta, chi, r1, r2):
    """
    Calculate second tensor equation ratio with more complex trigonometric terms
    
    Args:
        theta (float): Angle theta in radians
        chi (float): Angle chi in radians
        r1 (float): First ratio parameter
        r2 (float): Second ratio parameter
    
    Returns:
        float: Ratio of complex trigonometric expressions
    """
    # Calculate numerator: 2 * (sin²θ * cos²θ * (r₁cos²χ + r₂sin²χ - 1)² + sin²θ * sin²χ * cos²χ * (r₁ - r₂)²)
    numerator = 2 * (
            math.sin(theta) ** 2 * math.cos(theta) ** 2 * (r1 * math.cos(chi) ** 2 + r2 * math.sin(chi) ** 2 - 1) ** 2 +
            math.sin(theta) ** 2 * math.sin(chi) ** 2 * math.cos(chi) ** 2 * (r1 - r2) ** 2
    )

    # Calculate denominator: same as in your_function
    denominator = (
                          math.cos(theta) ** 2 * (r1 * math.cos(chi) ** 2 + r2 * math.sin(chi) ** 2) +
                          (r1 * math.sin(chi) ** 2 + r2 * math.cos(chi) ** 2) +
                          math.sin(theta) ** 2
                  ) ** 2

    result = numerator / denominator
    return result

def find_angles(r1, r2, target1, target2, tolerance=0.05):
    """
    Search for angles that satisfy the target values within given tolerance
    
    Args:
        r1 (float): First ratio parameter
        r2 (float): Second ratio parameter
        target1 (float): Target value for first function
        target2 (float): Target value for second function
        tolerance (float): Acceptable difference from target values
    
    Returns:
        tuple: First found (theta, chi) pair in degrees that satisfies conditions, or None if no solution found
    """
    # Iterate through angles from 0° to 720° in 1° increments
    for i in range(0, 721, 1):
        for j in range(0, 721, 1):
            theta_value = i / 360 * math.pi  # Convert to radians (i/2 degrees)
            chi_value = j / 360 * math.pi    # Convert to radians (j/2 degrees)
            
            # Check if the function values are close to target values
            func1 = your_function(theta_value, chi_value, r1, r2) - target1
            func2 = another_function(theta_value, chi_value, r1, r2) - target2
            
            # If both functions are within tolerance of their target values
            if abs(func1) < tolerance and abs(func2) < tolerance:
                # Return the first solution found
                return i/2, j/2  # Return angles in degrees
    
    return None

def main():
    """
    Main function to handle command line arguments and execute the angle search
    """
    parser = argparse.ArgumentParser(description='Find angles that satisfy tensor equations.')
    parser.add_argument('--r1', type=float, required=True, help='First ratio parameter')
    parser.add_argument('--r2', type=float, required=True, help='Second ratio parameter')
    parser.add_argument('--target1', type=float, required=True, help='Target value for first function')
    parser.add_argument('--target2', type=float, required=True, help='Target value for second function')
    parser.add_argument('--tolerance', type=float, default=0.05, help='Tolerance for target values (default: 0.05)')
    
    args = parser.parse_args()
    
    print(f"Searching for angles with parameters:")
    print(f"r1 = {args.r1}, r2 = {args.r2}")
    print(f"Target values: {args.target1}, {args.target2}")
    print(f"Tolerance: {args.tolerance}")
    print("This may take a few minutes...")
    
    result = find_angles(args.r1, args.r2, args.target1, args.target2, args.tolerance)
    
    if result is None:
        print("\nNo solutions found within the given tolerance.")
        return 1
    
    theta, chi = result
    theta_rad = theta * math.pi / 180
    chi_rad = chi * math.pi / 180
    
    print("\nFound solution:")
    print(f"theta = {theta:.2f}°")
    print(f"chi = {chi:.2f}°")
    print(f"Function values at solution:")
    print(f"f1 = {your_function(theta_rad, chi_rad, args.r1, args.r2):.4f}")
    print(f"f2 = {another_function(theta_rad, chi_rad, args.r1, args.r2):.4f}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
