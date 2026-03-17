## localized_defects_in_3d
**fieldplot.py:** plots the colormap of $E_z$

**intensityplot.py:** plots the 2d slice of $E_z$

**plotmeep.py:** plots MEEP band structure

**plotnonlinear.py:** plots the linear and nonlinear scaling of Q with system size

**rscanplot.py:** plots the scan of defect radius

**./plot_unit_cell.m:** plots the unit cell in matlab and saves the resulting image as a high resolution pdf.  

**./symeigs.ipynb:** Computes the symmetry eigenvalues of the bulk structure using the data created in the folder **./symeigs/**. The result of this code is used in **Figure 1** of the paper.  

**./defect_scan.ipynb**: Calculates the bands of the supercell structure as the defect size is tuned. In particular, it finds the parameter range at which a degeneracy is obtained between the singly degenerate defect band and the three-fold degenerate bulk band at the **R** point. 

**space_group_sweep_revised.ipynb**: Filtering of space groups for **Figure 4**. 
  - For an edge case that is not covered in the filtering above, see: https://hackmd.io/@aligho/B1_cX7bq-e 
