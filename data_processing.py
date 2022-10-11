import time
import tifffile as tif
import napari
from sols_microscope import DataPreview, DataNative, DataTraditional

def imread(filename): # re-define imread to keep 5D axes
    with tif.TiffFile(filename) as t:
        axes = t.series[0].axes
        hyperstack = t.series[0].asarray()
    return tif.transpose_axes(hyperstack, axes, 'TZCYX')

def imwrite(filename, data):
    return tif.imwrite(filename, data, imagej=True)

def view_in_napari(preview, voxel_aspect_ratio, traditional):
    print('\nViewing in napari')
    with napari.gui_qt():
        viewer_1 = napari.Viewer()
        viewer_1.add_image(preview, name='preview')
        viewer_2 = napari.Viewer()
        viewer_2.add_image(traditional[0,:,0,:,:], name='traditional')

# Get processsing tools:
datapreview     = DataPreview()
datanative      = DataNative()
datatraditional = DataTraditional()

# Get data and metadata:
t0 = time.perf_counter()
print('\nGetting: data', end=' ')
data = imread('data\data.tif')
t1 = time.perf_counter()
print('(%0.2fs)'%(t1 - t0))
print('-> data.shape =', data.shape)
print('-> format = 5D "tzcyx" (volumes, slices, channels, height_px, width_px)')
scan_step_size_px = 3
preview_line_px = 10
preview_crop_px = 0
timestamp_mode = "binary+ASCII"
voxel_aspect_ratio =  1.7320508075688772

# Get preview:
print('\nGetting: preview', end=' ')
preview = datapreview.get(
    data, scan_step_size_px, preview_line_px, preview_crop_px, timestamp_mode)
t2 = time.perf_counter()
print('(%0.2fs)'%(t2 - t1))
print('-> saving: data_preview.tif')
imwrite('data_preview.tif', preview)

if timestamp_mode != "off": data = data[:, :, :, 8:, :] # skip timestamp rows

# Get native data:
print('\nGetting: native view', end=' ')
native = datanative.get(data, scan_step_size_px)
t3 = time.perf_counter()
print('(%0.2fs)'%(t3 - t2))
##print('-> saving: data_native.tif')
##imwrite('data_native.tif', native)

# Get traditional data: -> this is very slow (about ~5min)
print('\nGetting: traditional view', end=' ')
traditional = datatraditional.get(native, scan_step_size_px)
t4 = time.perf_counter()
print('(%0.2fs)'%(t4 - t3))
##print('-> saving: data_traditional.tif')
##imwrite('data_traditional.tif', traditional)
traditional = traditional[:, 378:616, :, 420:870, :] # manually cropped
print('-> saving: data_traditional.tif')
imwrite('data_traditional.tif', traditional)

# View in napari (or checked saved data with ImageJ or similar):
view_in_napari(preview, voxel_aspect_ratio, traditional)
