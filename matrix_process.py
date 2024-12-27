# @Author:  Xiao-Han Xi, Yan-Ti Liu, Hao Ma
# -*- coding = 'utf-8' -*-
# @Time:2024/11/4 12:39
# @File: matrix_process.py
# @Software: PyCharm

'''
This algorithm processes matrix data from an Excel file containing Raman tensor components.
It performs eigenvalue calculations and ratio computations for both Raman tensor and Intensity data.
The results are saved to a new Excel file with calculated eigenvalues and ratios.

Usage:
    python matrix_process.py input.xlsx [output.xlsx]
    If output filename is not provided, it will append '_result' to the input filename
'''

import numpy as np
import pandas as pd
import argparse
import sys
import os

def process_matrix(input_file, output_file=None):
    """
    Process matrix data from input Excel file and save results to output file
    
    Args:
        input_file (str): Path to input Excel file
        output_file (str, optional): Path to output Excel file. If None, appends '_result' to input filename
    
    Returns:
        bool: True if processing successful, False otherwise
    """
    try:
        # Read Excel file containing matrix data
        table = pd.read_excel(input_file)
        
        # Extract A-tensor components (Axx, Axy, Ayy, Axz, Ayz, Azz)
        matcols = table[['Axx', 'Axy',	'Ayy',	'Axz',	'Ayz',	'Azz']].values
        # Stack finite values from each column vertically
        input_data = np.vstack([i[np.isfinite(i)] for i in matcols.T]).T

        # Initialize arrays for storing 3x3 matrices, eigenvalues, and ratios
        matrix = np.zeros((input_data.shape[0], 3,3))
        diag = np.zeros((input_data.shape[0], 3))    # Store eigenvalues
        rs = np.zeros((input_data.shape[0], 2))      # Store eigenvalue ratios

        # Process each row of input data
        for i in range(input_data.shape[0]):
            # Construct symmetric 3x3 matrix from input components
            matrix[i][0,0] = input_data[i][0]        # Axx
            matrix[i][0,1] = matrix[i][1,0] = input_data[i][1]  # Axy
            matrix[i][0,2] = matrix[i][2,0] = input_data[i][3]  # Axz
            matrix[i][1,2] = matrix[i][2,1] = input_data[i][4]  # Ayz
            matrix[i][1,1] = input_data[i][2]        # Ayy
            matrix[i][2,2] = input_data[i][5]        # Azz

            # Calculate eigenvalues for current matrix
            diag[i] = np.linalg.eigvals(matrix[i])
            # Calculate ratios of eigenvalues (normalized to largest eigenvalue)
            rs[i] = diag[i,0]/diag[i,2], diag[i,1]/diag[i,2]       

        # Extract I-tensor components and calculate their ratios
        Icols = table[['I/aa', 'I/ac',	'I/cc']].values
        I1, I2 = Icols[:, -1]/Icols[:, 0], Icols[:, 1]/Icols[:, 0]

        # Create output DataFrame with all calculated values
        # If I-tensor has more rows than A-tensor, pad with NaN values
        df = pd.DataFrame({
            'Freq1': table['Freq1'],
            'a_xx': [i for i in diag[:, 0]]+(len(I1)-diag.shape[0])*[np.nan],  # First eigenvalue
            'a_yy': [j for j in diag[:, 1]]+(len(I1)-diag.shape[0])*[np.nan],  # Second eigenvalue
            'a_zz': [k for k in diag[:, 2]]+(len(I1)-diag.shape[0])*[np.nan],  # Third eigenvalue
            'r_1': [m for m in rs[:, 0]]+(len(I1)-diag.shape[0])*[np.nan],     # First ratio
            'r_2': [n for n in rs[:, 1]]+(len(I1)-diag.shape[0])*[np.nan],     # Second ratio
            'Freq2': table['Freq2'],
            'I_1': [i1 for i1 in I1],    # I_1 = Icc/Iaa
            'I_2': [i2 for i2 in I2],    # I_2 = Iac/Iaa
        })

        # Determine output filename if not provided
        if output_file is None:
            base, ext = os.path.splitext(input_file)
            output_file = f"{base}_result{ext}"

        # Save results to output Excel file
        df.to_excel(output_file, sheet_name='Sheet1', index=False)
        print(f"Results saved to: {output_file}")
        return True

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """
    Main function to handle command line arguments and execute matrix processing
    """
    parser = argparse.ArgumentParser(description='Process matrix data from Excel file.')
    parser.add_argument('input_file', help='Input Excel file containing matrix data')
    parser.add_argument('output_file', nargs='?', help='Output Excel file (optional)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist")
        sys.exit(1)
    
    # Process the matrix data
    success = process_matrix(args.input_file, args.output_file)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
