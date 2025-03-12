from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
import requests

@register("tianmei_video", "Your Name", "甜妹视频插件", "1.0.0", "repo url")
class TianmeiVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("甜妹视频")
    async def get_tianmei_video(self, event: AstrMessageEvent):
        try:
            # 发送 GET 请求到接口地址
            response = requests.get("https://api.52vmy.cn/api/video/tianmei", timeout=10)
            response.raise_for_status()  # 检查请求是否成功

            # 解析返回的 JSON 数据
            data = response.json()
            if data["code"] == 200 and data["msg"] == "成功":
                video_url = data["data"]["video"]

                # 发送视频链接给用户
                yield event.plain_result(f"甜妹视频来啦！点击观看：\n{video_url}")
            else:
                yield event.plain_result("获取甜妹视频失败，服务器返回错误信息。")

        except requests.exceptions.RequestException as e:
            # 处理请求异常
            error_message = f"获取甜妹视频失败，可能是网络问题或接口调用失败。请稍后再试。错误信息：{str(e)}"
            yield event.plain_result(error_message)
        except Exception as e:
            # 处理其他异常
            error_message = f"获取甜妹视频时发生错误：{str(e)}"
            yield event.plain_result(error_message)
