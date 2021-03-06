from urllib.parse import urlencode

from nonebot import CommandSession, on_command

from app.config import Config
from app.models.user import User
from app.utils.api import to_token
from base64 import b64encode

__plugin_name__ = "绑定教务处"
__plugin_short_description__ = "命令：bind/unbind"

__plugin_usage__ = r"""
帮助链接：https://bot.artin.li/guide/bind.html

对我发以下关键词绑定教务处：
    - bind
    - 绑定
    - 绑定教务处

取消绑定教务处
使用方法：向我发送以下指令。
    - unbind
    - 取消绑定
    - 解绑
"""


@on_command("bind", aliases=("绑定", "绑定教务处"))
async def bind(session: CommandSession):
    web_url = Config.WEB_URL
    if not web_url:
        session.finish("绑定功能未启用")

    await session.send("开始请求绑定~ 请等待")

    sender_qq = session.event["user_id"]
    token = to_token(sender_qq)
    # web 登录界面地址
    query: str = urlencode({"qq": sender_qq, "token": token})
    encoded_query = b64encode(query.encode("utf8")).decode("utf8")
    url_ = f"{Config.WEB_URL}/login/?{encoded_query}"
    session.finish(f"请点击链接绑定：{url_}")


@on_command("unbind", aliases=("解绑", "取消绑定", "取消绑定教务处"))
async def unbind(session: CommandSession):
    r = await User.unbind(session.event["user_id"])
    if r:
        session.finish("取消绑定成功")
    session.finish("取消绑定失败")
