from rest_framework.pagination import PageNumberPagination

# 自定义分页控制类
class DynamicPagination(PageNumberPagination):
    # 默认每页显示数据条数
    page_size = 10
    # 指定客户端通过那个参数传递每页显示的数据条目
    page_size_query_param = 'size'
    # 每页显示的数据条数的最大值
    max_page_size = 100