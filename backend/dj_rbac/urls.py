from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from dj_rbac import settings
# drf-spectacular自带接口视图类
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
urlpatterns = [
    path('admin/', admin.site.urls),
    # 注册应用路由
    path('api/', include('system.urls')),
    # 媒体文件（客户头像、商品图、编辑器上传的图片）
    # 这里不用 django.conf.urls.static.static() —— 那个函数在 DEBUG=False 时直接返回空列表，
    # 结果就是"关掉调试模式后所有图片 404"。用 serve 显式挂上去，行为与 DEBUG 无关。
    # 生产环境应该交给 Nginx / 对象存储，别让 Django 送文件。
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# 在线接口文档（schema / swagger / redoc）
# 这三个视图原来写死了 authentication_classes=[]、permission_classes=[]，等于匿名可读。
# 它不是普通页面 —— 是一份写着所有接口、参数、字段结构的目录，扫描器最爱的入口。
# 所以默认跟 DEBUG 走：本机开发开着方便，部署到公网自动关掉；要强行开就设 ENABLE_API_DOCS=true。
if settings.ENABLE_API_DOCS:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(authentication_classes=[],permission_classes=[]), name='schema'),
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema',authentication_classes=[],permission_classes=[]), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema',authentication_classes=[],permission_classes=[]), name='redoc'),
    ]

# 开启debug调试模式的时候， 再挂上 debug toolbar
if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls
    urlpatterns = [
                      *urlpatterns,
                  ] + debug_toolbar_urls()
