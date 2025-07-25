from utils.logger import get_logger
logger = get_logger('mailer')
import datetime
import smtplib
import ssl
from email.message import EmailMessage

import config


def send_email(subject: str, text_content: str, html_content: str):
    try:
        logger.info(f"准备发送邮件，主题: {subject}")
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = config.EMAIL_SENDER
        msg["To"] = config.EMAIL_RECEIVER

        # 添加纯文本和 HTML 内容
        msg.set_content(text_content)
        msg.add_alternative(html_content, subtype="html")

        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(config.SMTP_SERVER, config.SMTP_PORT, context=context)
        server.login(config.EMAIL_SENDER, config.EMAIL_PASS)
        server.send_message(msg)

        logger.info("✅ 邮件发送成功！")

    except Exception as e:
        logger.error(f"❌ 邮件发送失败：{e}")

    finally:
        try:
            server.quit()
        except Exception as e:
            logger.warning(f"⚠️ 连接关闭时出错（可忽略）：{e}")


def build_html_report(weather: str, sentence: str) -> str:
    today = datetime.date.today()
    weekday = ["一", "二", "三", "四", "五", "六", "日"][today.weekday()]

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: "微软雅黑", sans-serif;
                color: #333;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .card {{
                max-width: 600px;
                margin: auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #4a90e2;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }}
            .weather, .sentence {{
                margin-top: 20px;
                line-height: 1.6;
                font-size: 16px;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #999;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📮 今日晨报~（{today} 周{weekday}）</h2>
            <div class="weather">
                <strong>📌 今日天气：</strong><br/>
                {weather.replace('\n', '<br/>')}
            </div>
            <div class="sentence">
                <strong>🌟 小记：</strong><br/>
                {sentence}
            </div>
            <div class="footer">
                今天也要继续开心~ ☀️
            </div>
        </div>
    </body>
    </html>
    """
    return html
