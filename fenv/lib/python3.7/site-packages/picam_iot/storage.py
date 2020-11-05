from os import path
from os import makedirs as mkdir
from os import remove as rm
from shutil import rmtree as rmdir
import dropbox as dbx
import posixpath
from dropbox.exceptions import ApiError

class local_storage:
    """ A class to manage local storage functionality.
    """
    def __init__(self, images_dir = './images/', videos_dir = './videos/'):
        """ Initializes the storage menagement class

        :param local: sets the target local storage. Default is the working directory
        
        """
        self.set_images_dir(images_dir)
        self.set_videos_dir(videos_dir)
    
    
    def set_images_dir(self, dir):
        """ Creates an image local directory
        :param dir: the path to the images local directory
        """
        if (path.exists(dir)):
            self.images_dir = dir
        else:
            mkdir(dir, exist_ok = True)
        self.images_dir = dir
    
    def set_videos_dir(self, dir):
        """ Creates local directory for videos
        :param dir: the path to the videos local directory
        """
        if (path.exists(dir)):
            self.videos_dir = dir
        else:
            mkdir(dir, exist_ok = True)
        self.videos_dir = dir
    
    def get_images_dir(self):
        """Returns the path to the images local directory

        :returns: the path to the images dirtectory
        :rtype: string
        """
        return self.images_dir
    
    def get_videos_dir(self):
        """Returns the path to the videos local directory

        :returns: the path to the videos dirtectory
        :rtype: string
        """
        return self.videos_dir
    
    def cleanup(self, images = True, videos = True):
        """Removes the local directories for the videos and images
        :param images: Remove the images dir
        :param videos: remove the videos dir
        """
        if images:
            rmdir(self.images_dir)
        if videos:
            rmdir(self.videos_dir)

class dropbox_storage:
    
    client = None

    def __init__(self, base = "/", access_token = None):
        """Initializez Dropbox and sets up the access token and the base path
        
        :param base: the dropbox app base path
        :param access_token: the dropbox app access token
        """
        self.base = base
        self.access_token = access_token
        if access_token:
            self.setup(access_token)
    
    def setup(self, access_token):
        """Setup the dropbox access token
        :param access_token: the dropbox app access token
        """
        self.client = dbx.Dropbox(access_token)
        images_path = posixpath.join(self.base + "images")
        if not self.path_exists(images_path):
            self.client.files_create_folder(images_path)

        videos_path = posixpath.join(self.base + "videos")
        if not self.path_exists(videos_path):
            self.client.files_create_folder(videos_path)
        
    
    def upload_image(self, name , local):
        """Uploads an image from a local path
        :param name: name of the image with the file type.
        :param local: the local image to upload.
        """
        dbx_path = f"{self.base}images/{name}"
        self.client.files_upload(open(local, "rb").read(), dbx_path)
    
    def upload_video(self, name, local):
        """Uploads a video from a local path
        :param name: name of the video with the file type.
        :param local: the local video to upload.
        """
        dbx_path = f"{self.base}videos/{name}"
        self.client.files_upload(open(local, "rb").read(), dbx_path)
    
    def path_exists(self, path):
        """Checks if a folder or a path exists on dropbox

        :param path: path to be checked
        :return: boolean indication of the existance of the path
        :rtype: boolean
        """
        try:
            self.client.files_get_metadata(path)
            return True
        except ApiError as e:
            if e.error.get_path().is_not_found():
                return False
            raise