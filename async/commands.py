import datetime
import pytz
import re

from utils import notion, helpers

today = datetime.datetime.now(pytz.timezone('US/Eastern'))
date_format = '%A (%-m/%-d/%Y)'


def create_metrics_page(driver, days_from_today='0'):
    driver.get('https://www.notion.so/sbue/e0dc488c21da4665b1ab8da3b9ef0e99?v=bf002a6098294df1ba026bd366f60b3c')
    notion.click_blue_new(driver)
    notion.click_open_as_page(driver)
    day = today + datetime.timedelta(days=int(days_from_today))
    notion.new_page_set_name(driver, day.strftime(date_format))
    notion.set_column_value(driver, column_type='calendar', column_name='Date', new_value=day.strftime('%-m/%-d/%Y'))
    with helpers.s3fs.open('metrics_url', 'wb') as fp:
        fp.write(driver.current_url.encode())


def create_planner_page(driver, days_from_today='0'):
    # TODO: copy from page template
    driver.get('https://www.notion.so/sbue/70cbc615e5a74e50a4159e2cdc3f020d?v=43296b27bdb046d7bd858f10d515e2e7')
    notion.click_blue_new(driver)
    notion.click_open_as_page(driver)
    day_title = (today + datetime.timedelta(days=int(days_from_today))).strftime(date_format)
    notion.new_page_set_name(driver, day_title)
    notion.set_column_value(driver, column_type='relation', column_name='🚒 Metrics', new_value=day_title)
    with helpers.s3fs.open('metrics_url', 'wb') as fp:
        fp.write(driver.current_url.encode())
    notion.set_page_as_favorite(driver)


def create_log_late(driver, description, severity):
    driver.get('https://www.notion.so/sbue/edca5ec31dce4dc69fea5e77555c7869?v=a9729293976546e28f4553d3a85728b8')
    if severity not in ['skipped', '5 min late', '5-15 min late', '15-30 min late', '30-90 min late']:
        raise ValueError(f'Not a valid severity for [log-late] command. Was "{severity}"')
    notion.click_blue_new(driver)
    notion.click_open_as_page(driver)
    notion.new_page_set_name(driver, description)
    notion.set_column_value(driver, column_type='select', column_name='Severity', new_value=severity)
    today_title = today.strftime(date_format)
    notion.set_column_value(driver, column_type='relation', column_name='Day', new_value=today_title)


def create_log_screen_time(driver, time):
    driver.get('https://www.notion.so/sbue/bf276d7a17e24bf3844df9f3b0c29a5f?v=45c7bdddf1154d5284f161bbba2d87e2')
    if re.compile('[0-9]{1,2}hr [0-9]{1,2}m').match(time) is None:
        raise ValueError(f'Invalid time for [log-screen-time] command. Was "{time}"')
    notion.click_blue_new(driver)
    notion.click_open_as_page(driver)
    notion.new_page_set_name(driver, time)
    today_title = today.strftime(date_format)
    notion.set_column_value(driver, column_type='relation', column_name='Day', new_value=today_title)


def create_log_cardio(driver, num_miles):
    driver.get('https://www.notion.so/sbue/22f169d5a17f42f98192bf02bf58b373?v=05189184b89f4a488fd24e5cd846c247')
    notion.click_blue_new(driver)
    notion.click_open_as_page(driver)
    notion.new_page_set_name(driver, num_miles)
    today_title = today.strftime(date_format)
    notion.set_column_value(driver, column_type='relation', column_name='Day', new_value=today_title)


def create_log_weight(driver, weight):
    driver.get('https://www.notion.so/sbue/6bed355e53544818a5deb972aa275d29?v=9747e738835247c5b0bb1fcbe3cd8114')
    notion.click_blue_new(driver)
    notion.click_open_as_page(driver)
    notion.new_page_set_name(driver, weight)
    today_title = today.strftime(date_format)
    notion.set_column_value(driver, column_type='relation', column_name='Day', new_value=today_title)


def set_metric_gym(driver, is_checked=True):
    with helpers.s3fs.open('metrics_url', 'rb') as fp:
        driver.get(fp.read().decode())
    notion.set_column_value(driver, column_type='checkbox', column_name='🏋', new_value=is_checked)


def set_metric_read(driver, is_checked=True):
    with helpers.s3fs.open('metrics_url', 'rb') as fp:
        driver.get(fp.read().decode())
    notion.set_column_value(driver, column_type='checkbox', column_name='📖', new_value=is_checked)


def set_metric_out_of_bed(driver, out_of_bed_time):
    with helpers.s3fs.open('metrics_url', 'rb') as fp:
        driver.get(fp.read().decode())
    notion.set_column_value(driver, column_type='text', column_name='🛏', new_value=out_of_bed_time)


def set_metric_productivity(driver, score):
    if score not in ['1', '2', '3', '4']:
        raise ValueError(f'Invalid score for [metric-productivity] command. Was "{score}"')
    with helpers.s3fs.open('metrics_url', 'rb') as fp:
        driver.get(fp.read().decode())
    notion.set_column_value(driver, column_type='select', column_name='📊', new_value=score)


def set_metric_happiness(driver, score):
    if score not in ['😔', '😕', '🙂', '😊']:
        raise ValueError(f'Invalid score for [metric-happiness] command. Was "{score}"')
    with helpers.s3fs.open('metrics_url', 'rb') as fp:
        driver.get(fp.read().decode())
    notion.set_column_value(driver, column_type='select', column_name='🧠', new_value=score)


commands_fns = {
    'new-metrics': create_metrics_page,
    'new-planner': create_planner_page,
    'log-late': create_log_late,
    'log-screen_time': create_log_screen_time,
    'log-cardio': create_log_cardio,
    'log-weight': create_log_weight,
    'metric-gym': set_metric_gym,
    'metric-read': set_metric_read,
    'metric-out-of-bed': set_metric_out_of_bed,
    'metric-productivity': set_metric_productivity,
    'metric-happiness': set_metric_happiness
}
