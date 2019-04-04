import tempfile
import time
import traceback

from fs.tools import copy_file_data
from zappa.asynchronous import task

from async.commands import commands_fns
from async.login import enter_notion
from utils import selenium
from utils.helpers import s3fs, current_env, logger, paths


@task
def execute_command_task(event, context):
    driver = selenium.get_driver()
    driver.manage().window().maximize();
    try:
        fn = commands_fns[event['command']]
        logger.info('Going to Notion.so')
        enter_notion(driver)
        logger.info(f'Enter command [{fn.__name__}]')
        fn(driver, **event['args'])
        logger.info(f'Finished command [{fn.__name__}]')
        time.sleep(0.5)
    except:
        if current_env == 'linux':
            for window in driver.window_handles:
                driver.switch_to_window(window)
                remote_path = f'{paths["screenshots"]}/{time.time()}-{fn.__name__}.png'
                with s3fs.open(remote_path, 'wb') as remote_file:
                    with tempfile.NamedTemporaryFile('rb+', suffix='.png') as local_file:
                        driver.save_screenshot(local_file.name)
                        copy_file_data(local_file, remote_file)
        logger.error(traceback.format_exc())
    finally:
        logger.info('Reached finally statement. Exiting program')
        driver.quit()
