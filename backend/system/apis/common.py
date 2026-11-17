import pathlib
import uuid
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from pypinyin import pinyin,Style

import qrcode
from io import BytesIO
from PIL import Image
from django.conf import settings
from django.http import HttpResponse

# 富文本编辑器允许上传的图片后缀（白名单，其余一律拒绝）
ALLOWED_IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
# 单张图片的体积上限：5MB（编辑器自身的 base64 临界值是 1MB）
MAX_IMAGE_SIZE = 5 * 1024 * 1024

# 工具接口类
class CommonViewSet(ViewSet):
    # 认证/权限沿用全局配置（CustomJwtAuth + CustomPermission），不再单独放行。
    # 这个类没有定义 rbac_permissions，所以只要求"已登录"，不再细分权限码 ——
    # 拼音转换、二维码、编辑器图片上传都是登录后的通用工具。
    # permission_classes = []
    # authentication_classes = []

    @action(['get'], detail=False)
    def get_spell(self, request):
        output = {'message': 'success'}
        # 获取查询参数
        words = request.query_params.get('words')
        if not words:
            output['message'] = '参数错误:缺少参数words'
            return Response(output, status=status.HTTP_200_OK)
        # 获取中文的拼音
        output['data'] = {
            'spell': [item[0] for item in pinyin(words, style=Style.NORMAL)],
            'first_spell': [item[0] for item in pinyin(words, style=Style.FIRST_LETTER)],
        }
        return Response(output)
    # /api/common/upload_image/
    # 图片上传接口
    @action(['post'], detail=False)
    def upload_image(self,request):
        # 接收客户端提交的文件对象
        file_obj = request.FILES.get('image')
        if not file_obj:
            return Response({'errno':1,'message': '参数错误:缺少参数image'})
        # 后缀白名单：不信任客户端给的完整文件名，只取后缀并限制在图片类型内
        file_ext=pathlib.Path(file_obj.name).suffix.lower()
        if file_ext not in ALLOWED_IMAGE_EXT:
            return Response({'errno':1,'message': f'不支持的文件类型：{file_ext or "无后缀"}'})
        # 体积上限：传大文件时 Content-Length 可能已被伪造，这里按实际读到的字节数判断
        if file_obj.size > MAX_IMAGE_SIZE:
            return Response({'errno':1,'message': f'图片超过 {MAX_IMAGE_SIZE // 1024 // 1024}MB 上限'})
        # 内容校验：后缀可以随便改，只查后缀等于允许把 .html 改名成 .jpg 传进来。
        # 用 Pillow 真解一遍文件头，解不开就不是图片。
        # verify() 会把文件指针移到末尾，所以校验完必须 seek(0) 再写盘。
        try:
            file_obj.seek(0)
            Image.open(file_obj).verify()
            file_obj.seek(0)
        except Exception:  # noqa: BLE001  截断文件、伪造头、非图片都会抛
            return Response({'errno':1,'message': '文件内容不是有效的图片'})
        # 落盘目录跟着 MEDIA_ROOT 走（绝对路径），不依赖启动时的工作目录
        dirname = pathlib.Path(settings.MEDIA_ROOT) / 'editor'
        dirname.mkdir(parents=True, exist_ok=True)
        # 文件名用 uuid：避免同一时间戳互相覆盖，也避免脏文件名带路径穿越
        filename = f"{uuid.uuid4().hex}{file_ext}"
        fullpath = dirname / filename
        with open(fullpath,'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        # 返回给前端的仍然是可直接访问的 URL，形如 /media/editor/xxx.png
        url = f"{settings.MEDIA_URL.rstrip('/')}/editor/{filename}"
        return Response({'errno':0,'data': {'url':url}})

    @action(['get'], detail=False)
    def make_qrcode(self,request):
         # 从 GET 参数中获取要编码的数据，例如 ?data=HelloWorld
        data = request.query_params.get('data')
        if not data:
            return Response({'message': '参数错误:缺少参数data'},status=status.HTTP_400_BAD_REQUEST)
        # 内容超长是"用户输入不合规"，不是服务器出错 —— 提前拦，别等 qrcode 抛出来变 500
        if len(data.encode('utf-8')) > 1800:
            return Response(
                {'message': '内容过长，二维码容纳不下（上限约 1800 字节），请缩短后再生成'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 创建二维码对象
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        try:
            qr.add_data(data)
            qr.make(fit=True)
        except ValueError:
            # 兜底：长度判定之外还有编码层面的边界情况
            return Response(
                {'message': '内容无法编码成二维码，请检查是否包含不支持的字符'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 生成图像
        img = qr.make_image(fill_color="black", back_color="white")

        # 将图像写入内存字节流
        buffer = BytesIO()
        # 将二维码图像以 PNG 格式保存到内存字节流中
        img.save(buffer, format="PNG")
        # 将指针移动到字节流开头，以便后续读取完整图像数据
        buffer.seek(0)

        # 返回 HttpResponse
        return HttpResponse(buffer.getvalue(), content_type="image/png")
