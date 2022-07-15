# SOLS_psf_data
An example of PSF data and processing for the original SOLS microscope.
## Summary:
A 3D matrix of randomly distributed fluorescent beads are embedded in a ~water refractive index gel and imaged at ~525nm with the typical SOLS setup (see **Details** below). The raw data is transformed back into the 'traditional' XYZ coordinates of a microscope, and cropped to form a rectangular cuboid (see **data_processing.py**).
Traditional volumes are then fed into **PSFj** for analysis.
- For the **whole volume** measuring ~118x52x28 um^3 (XYZ) we find 374 beads of median size:
  * **FWHM-XY min, FWHM-XY max= (285 +/- 4) nm, (315 +/- 7) nm**
  * **FWHM-Z = (857 +/- 44) nm**
  * Asymmetry = 0.917 +/- 0.024
- If we analyze a **central sub-stack** like data05.tif measuring ~118x96x2.5 um^3 (XYZ) then we find 15 beads of median size:
  * **FWHM-XY min, FWHM-XY max= (289 +/- 12) nm, (305 +/- 14) nm**
  * **FWHM-Z = (762 +/- 53) nm**
  * Asymmetry = 0.945 +/- 0.019
- We can **'cherry pick'** a central bead from the whole volume (for example 'bead_3' from data05.tif) to get:
  * **FWHM-XY min, FWHM-XY max= 276 nm, 293 nm**
  * **FWHM-Z = 737 nm**
  * Asymmetry = 0.945

See the included **.pdf reports** and **.csv files** for details.

## Reproduce:
To repeat the analysis:
- Download the whole repository.
- Get a copy of PSFj build 245 (https://github.com/amsikking/PSFj) and 'sols_microscope.py' from: https://github.com/amsikking/SOLS_microscope.
- Run 'make_data_file.py' in the data directory, followed by 'data_processing.py' and 'data05_processing.py' to generate 'data_traditional.tif' and 'data05_traditional.tif' -> **this is slow to run** (install Python dependencies as needed, napari is optional).
- Check out the **'preview'** files to see projections of the beads.
- Drag and drop the traditional volumes into PSFj and make sure to select the **"Use 3D localization"** option in the "Advanced settings..." tab. Note: PSFj should re-use the included **.ini** files for the analysis (if not simply copy the contents into the GUI or another .ini file).
- Set the **'Threshold'** to ~10x the background to reject noise and speed up the analysis (optionally copy exact numbers from included .pdf reports) and set the **sub-stack size** to 10 pixels to reduce bead crosstalk in the volume (**this step is slow!**).
- Generate the reports for the beads (copies included here).

## Details:
For the acquisition we used a 488 nm laser and 525/50nm emission filter with scan step size that gives a voxel aspect ratio of ~1.73 (see the included **'metadata.txt'** for more info).
- The sample position was adjusted so that the coverslip was at the bottom and just inside the volume (bottom of the top projection in the preview files).  For the sample preparation see https://github.com/amsikking/fluorescent_beads_in_agarose.
- The light-sheet slit (that controls it's NA) was set to ~0.5mm at the secondary objective back focal plane.
- Here the process we follow to transform the raw data into a traditional format (that PSFj can accept) results in many 'empty' pixels that we crop out manually in the processing scripts to reduce the file size and computational burden.
- For the microscope configuration we use the Nikon 100x1.35 Silicone objective as primary, with the Nikon 40x0.95 air objective as secondary and an AMS-AGY v1.0 objective (with a 30degree tilt) as the tertiary objective. See 'sols_microscope.py' and https://andrewgyork.github.io/high_na_single_objective_lightsheet/ for more details.
