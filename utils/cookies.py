import pickle

from utils.helpers import s3fs, paths


def load_cookies(driver, filename):
    if s3fs.exists(f'{paths["cookies"]}/{filename}'):
        cookies = pickle.load(s3fs.open(f'{paths["cookies"]}/{filename}', 'rb'))
        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                pass


def store_cookies(driver, filename):
    cookies_to_store = driver.get_cookies()
    pickle.dump(cookies_to_store, s3fs.open(f'{paths["cookies"]}/{filename}', 'wb'))
