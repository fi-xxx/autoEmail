from utils.logger import get_logger
logger = get_logger('main')
from utils.weather import get_weather

from utils.funny_sentence import get_sentence

from utils.mailer import send_email, build_html_report


def main():
    logger.info('程序启动')
    weather_info = get_weather()
    logger.info('天气信息获取完毕')
    sentence = get_sentence()
    logger.info('每日一句获取完毕')
    subject = "📮 早呀~"

    text = f"【今日天气】\n{weather_info}\n\n{sentence}"
    html = build_html_report(weather_info, sentence)

    send_email(subject, text, html)
    logger.info('邮件发送流程结束')


if __name__ == "__main__":
    main()
