"""
CLASSIFICATION MODULE

"""
import os
import sentinelsat as ss
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import matplotlib.pyplot as plt
from datetime import date
from osgeo import gdal
import numpy as np


class download_sentinel(object):
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.roi_polygon = None
        self.startdate = None
        self.enddate = None
        self.list_products = None

    def sentinel(self, download_type='ROI_polygon', roi_polygon=None, startdate=None, enddate=None, cloudcover_max=5,
                 platformname='Sentinel-2'):
        '''

        :param download_type:
        :param username:
        :param password:
        :param roi_polygon:
        :param startdate:
        :param enddate:
        :param cloudcover_max:
        :param platformname:
        :return:
        '''

        if startdate:
            self.startdate = startdate
        if enddate:
            self.enddate = enddate

        if roi_polygon:
            self.roi_polygon = roi_polygon
        self.api = SentinelAPI(self.username, self.password, 'https://scihub.copernicus.eu/dhus')

        product_id = None
        if download_type == 'full':
            if product_id:
                self.api.download(product_id)
            else:
                print('product id required')

        if download_type == 'ROI_polygon':
            if roi_polygon.split('.')[-1] == 'geojson':
                footprint = geojson_to_wkt(read_geojson(self.roi_polygon))

                products = self.api.query(footprint,
                                          date=(self.startdate, self.enddate),
                                          platformname='Sentinel-2',
                                          cloudcoverpercentage=(0, cloudcover_max))
                self.list_products = list(products.items())

    def download_files(self, list_product_ids):
        for product_id in list_product_ids:
            self.api.download(product_id)


class download_modis(object):
    """

    TBD
    :return:
    """

    def __init__(self):
        """
        """


class read_modis(object):
    def __init__(self, hdf_data_path):
        self.hdf_data_path = hdf_data_path
        df = gdal.Open(self.hdf_data_path, gdal.GA_ReadOnly)
        self.meta_data = df.GetMetadata()
        self.sdf = df.GetSubDatasets()
        self.band_details = [self.sdf[i][1] for i in range(len(self.sdf))]
        self.num_bands = len(self.sdf)
        self.img_shp = gdal.Open(self.sdf[0][0]).ReadAsArray().shape
        self.AOI = None
        self.data = None

    def get_data(self):
        self.data = np.zeros((self.img_shp[0], self.img_shp[1], self.num_bands))
        for i in range(self.num_bands):
            self.data[:, :, i] = gdal.Open(self.sdf[i][0]).ReadAsArray()

    def save_as_npy(self, save_folder=os.getcwd()):
        np.save(save_folder + '/data', self.data)
        print('dataset saved in .npy format at this location:', save_folder)




    