## localized_defects_in_3d
**./plotting/fieldplot.py:** plots the colormap of $E_z$. Note that the loaded dataset is $400\times 400\times 400$. With a resolution of $16$, this corresponds to ranges in each Cartesian coordinate of $-12.5$ to $12.5$

**./plotting/intensityplot.py:** plots the 2d slice of $E_z$. The loaded dataset is $496\times 496\times496$, corresponding to a $31\times31\times31$ supercell. 

**./plotting/plotmeep.py:** plots MEEP band structure
  - **./plotting/new_fig2a_data.ipynb**: Plots latest band structure data (the data file used by this notebook is available in the subdirectory, **./data**). 

**./plotting/plotnonlinear.py:** plots the linear and nonlinear scaling of Q with system size

**./plotting/rscanplot.py:** plots the scan of defect radius

**./plot_unit_cell.m:** plots the unit cell in matlab and saves the resulting image as a high resolution pdf.  

**./symeigs.ipynb:** Computes the symmetry eigenvalues of the bulk structure using the data created in the folder **./symeigs/**. The result of this code is used in **Figure 1** of the paper.  

**./defect_scan.ipynb**: Calculates the bands of the supercell structure as the defect size is tuned. In particular, it finds the parameter range at which a degeneracy is obtained between the singly degenerate defect band and the three-fold degenerate bulk band at the **R** point. 

**space_group_sweep_revised.ipynb**: Filtering of space groups for **Figure 4**. 
  - For an edge case that is not covered in the filtering above, see: https://hackmd.io/@aligho/B1_cX7bq-e
    -   A pdf of this is in **./pdfs_of_notes/**
  - To see how space group 166 may be written as a subgroup of space group 227, see: https://hackmd.io/@aligho/ryO1VHDiWx
