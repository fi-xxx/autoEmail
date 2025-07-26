from utils.logger import get_logger

import requests
import random
from requests.exceptions import RequestException
import config

logger = get_logger('weather')


def fetch_weather_data():
    """
    获取天气的原始数据字典，失败时返回None。
    """
    try:
        logger.info('请求天气API...')
        url = "https://" + config.WEATHER_API_HOST + config.WEATHER_CONST_PATH
        params = {
            "location": config.LOCATION_CODE,
            "key": config.WEATHER_API_KEY
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get("code") != "200":
            logger.warning(f"天气API返回异常: {data}")
            return None
        day = data['daily'][0]
        logger.info(f"天气API调用成功: {day}")
        return day

    except RequestException as e:
        logger.error(f"天气API请求异常: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        logger.error(f"天气API数据解析异常: {e}")
        return None
    except Exception as e:
        logger.error(f"天气API未知异常: {e}")
        return None


def format_weather_str(day):
    """
    将天气数据字典格式化为字符串。
    """
    if not day:
        funny_error_messages = [
            "☔ 糟糕，天气预报被风吹走了！请稍后再试~",
            "🌪️ 天气小精灵迷路了，暂时无法提供预报！",
            "🔮 水晶球模糊了，看不清天气...（网络错误）",
            "🐌 蜗牛快递员送天气数据太慢，超时了！",
            "🤖 机器人：'我尽力了，但天气API不理我...'",
            "🌩️ 雷公电母在开会，暂时无法获取天气~",
        ]
        return random.choice(funny_error_messages)

    weather_str = (
        f"📅 日期：{day['fxDate']}\n"
        f"⛅ 天气：{day['textDay']}\n"
        f"🌡️ 温度：{day['tempMin']}°C ~ {day['tempMax']}°C\n"
        f"💧 湿度：{day.get('humidity', '未知')}%\n"
        f"🌧️ 降水量：{day.get('precip', 0)}mm"
    )
    return weather_str


def generate_weather_reminder(weather):
    reminders = []

    if not weather:
        return "本来还想提醒你注意点天气呢，可惜我这里好像出了点问题T_T"

    # 解析主要字段
    try:
        temp_min = int(float(weather.get('tempMin', 0)))
    except Exception:
        temp_min = 0
    try:
        temp_max = int(float(weather.get('tempMax', 0)))
    except Exception:
        temp_max = 0
    try:
        precip = float(weather.get('precip', 0))
    except Exception:
        precip = 0
    try:
        humidity = int(float(weather.get('humidity', 0)))
    except Exception:
        humidity = 0
    try:
        uv_index = int(float(weather.get('uvIndex', 0)))
    except Exception:
        uv_index = 0
    try:
        wind_scale = int(float(weather.get('windScaleDay', 0)))
    except Exception:
        wind_scale = 0
    text_day = weather.get('textDay', '')

    # 温度相关
    if temp_max <= 5:
        reminders.append("今天好冷呀，记得多穿点哦，别冻着啦！🥶")
    elif temp_max <= 12:
        reminders.append("天气有点冷，出门一定要穿厚外套哦，注意保暖，抱抱你~")
    elif temp_max <= 20:
        reminders.append("有点凉，记得加件外套，别感冒啦！")
    elif temp_max >= 32:
        reminders.append("今天超级热，记得多喝水，防晒防中暑，少吃冰哦！☀️")
    elif temp_max >= 28:
        reminders.append("天气有点热，出门记得带伞防晒，多喝点水，我很想你~")
    else:
        reminders.append("温度刚刚好，适合约会和散步，想和你一起出去玩~")

    # 天气状况
    if '雨' in text_day:
        if precip > 10:
            reminders.append("今天雨有点大，出门一定要带伞，路上小心，最好别淋湿啦！")
        else:
            reminders.append("今天有雨，记得带伞哦，别让小雨淋湿你~")
    elif '雪' in text_day:
        reminders.append("下雪啦，地面滑，走路慢点，注意安全，想和你一起看雪~")
    elif '晴' in text_day:
        reminders.append("阳光很好，记得涂防晒，晒晒太阳心情会更好哦！")
    elif '阴' in text_day:
        reminders.append("天气有点阴沉，记得保持好心情，有我陪你不怕哦~")

    # 风力
    if wind_scale >= 5:
        reminders.append("风有点大，头发会乱哦，注意防风，别着凉啦！")

    # 湿度
    if humidity >= 80:
        reminders.append("今天有点潮湿，记得多通风，心情也要干爽哦~")
    elif humidity <= 30:
        reminders.append("空气有点干，记得多喝水，润润嗓子~")

    # 紫外线
    if uv_index >= 7:
        reminders.append("紫外线有点强，出门一定要涂防晒霜，保护好皮肤！")

    # 默认
    if not reminders:
        reminders.append("今天一切都刚刚好，和你在一起就很美好~")

    return "温馨提醒：\n" + "\n".join(reminders)


def get_weather():
    """
    获取格式化的天气信息和温馨提醒，供主程序调用。
    返回: (str) 适合文本和HTML展示的天气+提醒内容
    """
    day = fetch_weather_data()
    weather_text = format_weather_str(day)
    reminder_text = generate_weather_reminder(day)
    return f"{weather_text}\n\n{reminder_text}"
