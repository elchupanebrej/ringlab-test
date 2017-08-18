import pytest

from lib.NASA_rover_API import NASARoverAPI
from lib.date_sol import add_sol_to_date


@pytest.fixture
def rover_api():
    return NASARoverAPI(api_key='OoGI0ESgVHKxbkD4IRrUmJ1XEu2KwMlvp0LUuZ2K')


@pytest.mark.meta
@pytest.mark.parametrize('sol', [1000])
def test_image_meta_on_sol(sol, rover_api):
    sol_image_metas = rover_api.get_image_metas_by_sol(sol)
    earth_date_metas = rover_api.get_image_metas_by_date(add_sol_to_date(rover_api.rover.landing_date, sol))
    assert sol_image_metas == earth_date_metas


@pytest.mark.meta
@pytest.mark.parametrize('sol, ratio', [(1000, 10)])
def test_cam_counts_on_sol(sol, ratio, rover_api):
    image_metas = rover_api.get_image_metas_by_sol(sol)

    images_split_by_cam = [
        (camera_name, len(list(filter(lambda image_meta: image_meta['camera']['name'] == camera_name, image_metas))))
        for camera_name in [camera.name for camera in rover_api.rover.cameras]
    ]

    ordered_images_split_by_cam = sorted(images_split_by_cam, key=lambda x: x[1])
    normalization_camera_name, normalization_factor = ordered_images_split_by_cam[0]
    if normalization_factor == 0:
        failed_cameras = list(filter(lambda camera_with_count: camera_with_count[1] > 0, ordered_images_split_by_cam))
        assert not failed_cameras, "Cameras has infinity ratio to camera with name: {cam_name}, " \
                                   "images_count {images_count}\n" \
                                   "camera names, image count:{failed_cameras}".format(cam_name=normalization_camera_name,
                                                                                       images_count=normalization_factor,
                                                                                       failed_cameras=failed_cameras)

    normalized_images_split_by_cam = [(*ordered_images_split_by_cam, images_by_cam[1]/normalization_factor)
                                      for images_by_cam in ordered_images_split_by_cam]

    failed_cameras = list(filter(lambda camera_with_ratio: camera_with_ratio[2] > ratio, normalized_images_split_by_cam))

    assert not failed_cameras, "Ratios for cameras are higher than expected\n"\
                               "list of cameras with names, images count and ratios: {failed_cameras} \n" \
                               "to camera with lowest images count; camera name: {cam_name}, " \
                               "images_count {images_count}".format(failed_cameras=dict(failed_cameras),
                                                                    cam_name=normalization_camera_name,
                                                                    images_count=normalization_factor)

