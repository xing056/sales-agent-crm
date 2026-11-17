# 将扁平列表转为树形列表
"""
将扁平列表转换为树形结构。
:param nodes: 扁平列表，每个元素是 dict
:param id_key: 节点唯一标识字段名
:param parent_key: 父节点字段名（根节点该字段为 None 或 0）
:param children_key: 子节点列表字段名
:return: 树形列表
"""
from system.models import Menu
from ..models import Permission

def build_tree(nodes, id_key="id", parent_key="parent_id", children_key="children"):
    # 创建 id -> node 的映射，并初始化 children
    node_map = {}
    # 通过循环给每个对象添加一个列表属性用于存放子级节点数据,
    # 并将每个数据对象都添加到node_map字典中, 并以当前数据id作为属性名
    for node in nodes:
        # 将原始数据拷贝一份:避免修改原数据
        node = node.copy()
        # 添加一个属性, 用于存放子级节点数据
        node[children_key] = []
        # 将当前数据保存到node_map中
        node_map[node[id_key]] = node
    # 创建一个空列表
    tree = []
    # 再次对原始数据列表进行循环
    for node in nodes:
        # 获取原始数据的父级数据id
        parent_id = node[parent_key]
        if parent_id is None or parent_id not in node_map:
            # 根节点(一级节点)
            tree.append(node_map[node[id_key]])
        else:
            # 添加到父节点的 children
            node_map[parent_id][children_key].append(node_map[node[id_key]])
    return tree


# 根据用户对象获取用户菜单数据
# user: 用户对象
def get_user_menu(user):
    roles = []
    # 获取用户对象的角色信息
    # 查询角色表
    for role in user.role.all():
        # 查询权限数据
        # 循环查询权表
        # 使用prefetch_related方法之后， 此处不再执行数据库查询
        per_ids = [per.id for per in (Permission.objects.all() if user.is_superuser else role.permission.all())]
        # 根据权限id获取菜单数据
        all_menu = Menu.objects.filter(permission_id__in=per_ids).values()
        # 筛选主导航中需要显示的菜单
        nav_menu = [item for item in all_menu if item["menu_type"] in ["dir", "nav"]]
        # 获取已经查询出来的菜单id
        exists_menu_ids = [item["id"] for item in all_menu]
        # 查询菜单父级菜单数据, 目的是生成带层级结构的树状列表, 方便前端展示
        # 只超找nav和dir类型的父级菜单
        menu_parent_ids = set(
            [
                item["parent_id"]
                for item in all_menu
                if item["parent_id"] not in exists_menu_ids and item['menu_type'] in ['dir','nav']
            ]
        )
        # 将查询出来的父级菜单数据和已有的菜单列表合并
        nav_menu += Menu.objects.filter(id__in=menu_parent_ids).values()
        # 按钮菜单
        # btn_menu = [item['permission_code'] for item in all_menu if item['menu_type'] == 'btn']
        btn_menu, link_url = [], []
        for item in all_menu:
            # ** 登录之后返回所有的按钮 和 链接的 权限编码 **: 否则员工详情页面的按钮无法展示
            if item["menu_type"] == "btn" or item['menu_type']=='link':
                btn_menu.append(item["permission_code"])
            if item["menu_type"] == "nav" or item["menu_type"] == "link":
                link_url.append(item["path"])
        # build_tree: 将一个扁平列表转换成树状列表
        roles.append(
            {
                "id": role.id,
                "name": role.name,
                "nav_menu": build_tree(list(nav_menu)),
                "btn_menu": btn_menu,
                'link_url':link_url
            }
        )
    return roles
