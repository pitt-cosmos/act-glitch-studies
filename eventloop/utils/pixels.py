import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import moby2

class PixelReader:
    def __init__(self, season='2016', array='AR3', mask=None):
        self._array_info = {
            'season': season,
            'array_name': array
        }
        self._array_pos = None
        self._freqs = None
        self._array_data = moby2.scripting.get_array_data(self._array_info)
        self._pixel_dict = self.generate_pixel_dict()
        self._mask = mask
        #self.get_adjacent_detectors = self.adjacent_detector_generator()

    def generate_pixel_dict(self):
        """ Generate pixel dictionary that tells which detectors correspond
        to which pixel and frequencies """
        self._array_pos = np.vstack([self._array_data['array_x'], self._array_data['array_y']]).T
        self._freqs = np.sort(np.unique(ardata['nom_freq']))[1:]  # gather freqs (exclude 0)
        pixel_dict = {}  # initialize empty pixel_dict

        for det_id in self._array_data['det_uid']:
            if np.all(self._array_pos[det_id,:]==[0,0]):  # not physical
                continue
            if (self._array_data['det_type'][det_id] != 'tes'):  # remove non-tes
                continue
            dets = np.where(np.all(self._array_pos == self._array_pos[det_id,:],axis=1))[0]
            # make a dictionary of frequencies: f1: lower freq, f2: higher freq
            pol_dict = {
                'f1': [i for i in dets if self._array_data['nom_freq'][i]==self._freqs[0]],
                'f2': [i for i in dets if self._array_data['nom_freq'][i]==self._freqs[1]]
            }
            pixel_id = dets[0]  # index pixel by the smallest det_uid
            pixel_dict[str(pixel_id)]=pol_dict
            
        return pixel_dict
        
    def adjacent_detector_generator(self):
        """
        Generate a get_adjacent_pixels function
        Return a function to get adjacent detectors

        return: [int] function(int det)
        """
        # Get data from file
        ar = np.vstack([self._array_data['array_x'], self._array_data['array_y']]).T
        self._ar = ar  # store the array_x array_y data into a variable in the obj

        # Find the adjacent detectors
        adj_dets = [None] * len(self._array_data['array_x']) # Generate an empty list to store adjacent detector lists

        for i in range(len(self._array_data)):
            dis = np.dot((ar - ar[i,:])**2,[[1],[1]])
            _mask = ((dis < 0.6) & (dis > 0)).T & ((ar[:,0]!=0) | (ar[:,1]!=0))
            mask = _mask.flatten()
            indexes = np.where(mask == True)
            adj_dets[i]= list(list(indexes)[0]) # Normalize the np array output to list

        # Generate a function to access the data to make sure above procedures run once only
        def get_adjacent_detectors(detector):
            return adj_dets[detector]

        return get_adjacent_detectors

    def get_pixels(self, mask=None):
        return [int(key) for key in self._pixel_dict]

    def get_f90(self, pixel):
        if self._mask is not None:
            return [det for det in self._pixel_dict[str(pixel)]['f90'] if self._mask[det]==1]
        else:
            return self._pixel_dict[str(pixel)]['f90']
    
    def get_f150(self, pixel):
        if self._mask is not None:
            return [det for det in self._pixel_dict[str(pixel)]['f150'] if self._mask[det]==1]
        else:
            return self._pixel_dict[str(pixel)]['f150'] 
    
    def get_adjacent_pixels(self, pixel):
        all_adj_det = self.get_adjacent_detectors(pixel)
        return [int(det) for det in all_adj_det if str(det) in self._pixel_dict]
    
    def get_pixels_within_radius(self, pixel, radius):
        ar = self._ar
        dist = np.sqrt(np.sum((ar - ar[pixel,:])**2, axis=1))
        return [det for det in np.arange(1055)[dist<radius] if str(det) in self._pixel_dict]
        
    def plot(self, pixels=None):
        plt.plot(self._array_data['array_x'], self._array_data['array_y'],'r.')
        if pixels:
            plt.plot(self._array_data['array_x'][pixels], self._array_data['array_y'][pixels],'b.')

    def get_xy(self, pixel):
        return [self._array_data['array_x'][pixel], self._array_data['array_y'][pixel]]

    def get_x(self, pixel):
        return self._array_data['array_x'][pixel]

    def get_y(self, pixel):
        return self._array_data['array_y'][pixel]
