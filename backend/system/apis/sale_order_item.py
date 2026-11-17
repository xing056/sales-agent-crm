from rest_framework import viewsets,mixins
from rest_framework import status
from rest_framework.response import Response
from ..serializers import SaleOrderItemSerializer
from ..models import SaleOrderItem
# 订单商品接口类
class SaleOrderItemViewSet(viewsets.GenericViewSet,mixins.ListModelMixin):
    queryset =  SaleOrderItem.objects.all()
    serializer_class = SaleOrderItemSerializer
    rbac_permissions = {
        'list': 'api:sale_order_item:list'
    }
    # 禁用分类功能
    pagination_class = None
    # 临时禁用登录认证和权限类
    # authentication_classes=[]
    # permission_classes=[]
    # 获取订单商品数据
    def list(self,request,*args,**kwargs):
        # 订单id
        order_id = request.query_params.get('order_id')
        if not order_id:
            return Response({'message':'参数错误:order_id不能为空'},status=status.HTTP_400_BAD_REQUEST)
        queryset = self.filter_queryset(self.get_queryset()).filter(order_id=order_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

