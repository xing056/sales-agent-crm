---
title: rbac接口文档
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.30"

---

# rbac接口文档

基于django的rbac权限控制后端数据接口

Base URLs:

* <a href="http://localhost:8000">开发环境: http://localhost:8000</a>

# Authentication

# 菜单管理

<a id="opIdmenu_list"></a>

## GET 菜单列表

GET /api/menu/

获取菜单列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer| 否 |A page number within the paginated result set.|

> 返回示例

> 200 Response

```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "children": "string",
      "permission_id": -2147483648,
      "permission_code": "string",
      "title": "string",
      "path": "string",
      "icon": "string",
      "sort_order": -32768,
      "menu_type": "dir",
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z",
      "parent": 0
    }
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[PaginatedMenuList](#schemapaginatedmenulist)|

<a id="opIdmenu_create"></a>

## POST 新增菜单

POST /api/menu/

新增菜单数据

> Body 请求参数

```json
{
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "parent": 0
}
```

```yaml
permission_id: -2147483648
permission_code: string
title: string
path: string
icon: string
sort_order: -32768
menu_type: dir
parent: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[Menu](#schemamenu)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "children": "string",
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z",
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Menu](#schemamenu)|

<a id="opIdmenu_retrieve"></a>

## GET 菜单详情

GET /api/menu/{id}/

获取单条用户数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this menu.|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "children": "string",
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z",
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Menu](#schemamenu)|

<a id="opIdmenu_update"></a>

## PUT 更新菜单

PUT /api/menu/{id}/

更新菜单信息

> Body 请求参数

```json
{
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "parent": 0
}
```

```yaml
permission_id: -2147483648
permission_code: string
title: string
path: string
icon: string
sort_order: -32768
menu_type: dir
parent: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this menu.|
|body|body|[Menu](#schemamenu)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "children": "string",
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z",
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Menu](#schemamenu)|

<a id="opIdmenu_partial_update"></a>

## PATCH 菜单信息(部分更新)

PATCH /api/menu/{id}/

更新菜单信息中的部分属性字段

> Body 请求参数

```json
{
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "parent": 0
}
```

```yaml
permission_id: -2147483648
permission_code: string
title: string
path: string
icon: string
sort_order: -32768
menu_type: dir
parent: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this menu.|
|body|body|[PatchedMenu](#schemapatchedmenu)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "children": "string",
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z",
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Menu](#schemamenu)|

<a id="opIdmenu_destroy"></a>

## DELETE 删除菜单

DELETE /api/menu/{id}/

删除菜单数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this menu.|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

# 权限管理

<a id="opIdpermission_list"></a>

## GET 权限列表

GET /api/permission/

获取权限列表

> 返回示例

> 200 Response

```json
[
  {
    "id": 0,
    "children": "string",
    "name": "string",
    "code": "string",
    "url": "string",
    "method": "string",
    "status": true,
    "parent": 0
  }
]
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|[[Permission](#schemapermission)]|false|none||none|
|» id|integer|true|read-only||none|
|» children|string|true|read-only||none|
|» name|string|true|none|权限名称|none|
|» code|string|true|none|权限编码|none|
|» url|string¦null|false|none|接口地址|none|
|» method|string¦null|false|none|接口请求方式|none|
|» status|boolean|false|none|权限状态|none|
|» parent|integer¦null|false|none||none|

<a id="opIdpermission_create"></a>

## POST 新增权限

POST /api/permission/

新增权限数据

> Body 请求参数

```json
{
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

```yaml
name: string
code: string
url: string
method: string
status: true
parent: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[Permission](#schemapermission)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "children": "string",
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Permission](#schemapermission)|

<a id="opIdpermission_retrieve"></a>

## GET 权限详情

GET /api/permission/{id}/

获取单条角色数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this permission.|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "children": "string",
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Permission](#schemapermission)|

<a id="opIdpermission_update"></a>

## PUT 更新权限

PUT /api/permission/{id}/

更新权限信息

> Body 请求参数

```json
{
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

```yaml
name: string
code: string
url: string
method: string
status: true
parent: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this permission.|
|body|body|[Permission](#schemapermission)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "children": "string",
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Permission](#schemapermission)|

<a id="opIdpermission_partial_update"></a>

## PATCH 权限信息(部分更新)

PATCH /api/permission/{id}/

更新角色信息中的部分属性字段

> Body 请求参数

```json
{
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

```yaml
name: string
code: string
url: string
method: string
status: true
parent: 0

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this permission.|
|body|body|[PatchedPermission](#schemapatchedpermission)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "children": "string",
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Permission](#schemapermission)|

<a id="opIdpermission_destroy"></a>

## DELETE 删除权限

DELETE /api/permission/{id}/

删除权限数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this permission.|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

# 角色管理

<a id="opIdrole_list"></a>

## GET 角色列表

GET /api/role/

获取角色列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer| 否 |A page number within the paginated result set.|

> 返回示例

> 200 Response

```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[PaginatedRoleList](#schemapaginatedrolelist)|

<a id="opIdrole_create"></a>

## POST 新增角色

POST /api/role/

新增角色数据

> Body 请求参数

```json
{
  "permission_ids": [
    0
  ],
  "name": "string",
  "remark": "string",
  "status": true
}
```

```yaml
permission_ids:
  - 0
name: string
remark: string
status: true

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[Role](#schemarole)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "permission": [
    {
      "id": 0,
      "children": "string",
      "name": "string",
      "code": "string",
      "url": "string",
      "method": "string",
      "status": true,
      "parent": 0
    }
  ],
  "name": "string",
  "remark": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[Role](#schemarole)|

<a id="opIdrole_retrieve"></a>

## GET 角色详情

GET /api/role/{id}/

获取单条角色数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this role.|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "permission": [
    {
      "id": 0,
      "children": "string",
      "name": "string",
      "code": "string",
      "url": "string",
      "method": "string",
      "status": true,
      "parent": 0
    }
  ],
  "name": "string",
  "remark": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Role](#schemarole)|

<a id="opIdrole_update"></a>

## PUT 更新角色

PUT /api/role/{id}/

更新角色信息

> Body 请求参数

```json
{
  "permission_ids": [
    0
  ],
  "name": "string",
  "remark": "string",
  "status": true
}
```

```yaml
permission_ids:
  - 0
name: string
remark: string
status: true

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this role.|
|body|body|[Role](#schemarole)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "permission": [
    {
      "id": 0,
      "children": "string",
      "name": "string",
      "code": "string",
      "url": "string",
      "method": "string",
      "status": true,
      "parent": 0
    }
  ],
  "name": "string",
  "remark": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Role](#schemarole)|

<a id="opIdrole_partial_update"></a>

## PATCH 角色信息(部分更新)

PATCH /api/role/{id}/

更新角色信息中的部分属性字段

> Body 请求参数

```json
{
  "permission_ids": [
    0
  ],
  "name": "string",
  "remark": "string",
  "status": true
}
```

```yaml
permission_ids:
  - 0
name: string
remark: string
status: true

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this role.|
|body|body|[PatchedRole](#schemapatchedrole)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "permission": [
    {
      "id": 0,
      "children": "string",
      "name": "string",
      "code": "string",
      "url": "string",
      "method": "string",
      "status": true,
      "parent": 0
    }
  ],
  "name": "string",
  "remark": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Role](#schemarole)|

<a id="opIdrole_destroy"></a>

## DELETE 删除角色

DELETE /api/role/{id}/

删除角色数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this role.|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

# 用户管理

<a id="opIduser_list"></a>

## GET 用户列表

GET /api/user/

获取用户列表接口

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer| 否 |A page number within the paginated result set.|

> 返回示例

> 200 Response

```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "role": [
        {
          "id": 0,
          "permission": [
            {}
          ],
          "name": "string",
          "remark": "string",
          "status": true,
          "update_time": "2019-08-24T14:15:22Z",
          "create_time": "2019-08-24T14:15:22Z"
        }
      ],
      "username": "string",
      "phone": "string",
      "email": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[PaginatedUserList](#schemapaginateduserlist)|

<a id="opIduser_create"></a>

## POST 新增用户

POST /api/user/

新增用户数据

> Body 请求参数

```json
{
  "role_ids": [
    0
  ],
  "password": "string",
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true
}
```

```yaml
role_ids:
  - 0
password: string
username: string
phone: string
email: string
status: true

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 201 Response

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|201|[Created](https://tools.ietf.org/html/rfc7231#section-6.3.2)|none|[User](#schemauser)|

<a id="opIduser_retrieve"></a>

## GET 用户详情

GET /api/user/{id}/

获取单个用户数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this user.|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIduser_update"></a>

## PUT 更新用户

PUT /api/user/{id}/

更新用户信息

> Body 请求参数

```json
{
  "role_ids": [
    0
  ],
  "password": "string",
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true
}
```

```yaml
role_ids:
  - 0
password: string
username: string
phone: string
email: string
status: true

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this user.|
|body|body|[User](#schemauser)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIduser_partial_update"></a>

## PATCH 用户信息(部分更新)

PATCH /api/user/{id}/

更新用户信息中的部分属性字段

> Body 请求参数

```json
{
  "role_ids": [
    0
  ],
  "password": "string",
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true
}
```

```yaml
role_ids:
  - 0
password: string
username: string
phone: string
email: string
status: true

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this user.|
|body|body|[PatchedUser](#schemapatcheduser)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|

<a id="opIduser_destroy"></a>

## DELETE 删除用户

DELETE /api/user/{id}/

删除用户数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |A unique integer value identifying this user.|

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|204|[No Content](https://tools.ietf.org/html/rfc7231#section-6.3.5)|No response body|None|

<a id="opIduser_login_create"></a>

## POST 用户登录

POST /api/user/login/

用户登录接口

> Body 请求参数

```json
{
  "username": "string",
  "password": "string"
}
```

```yaml
username: string
password: string

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[Login](#schemalogin)| 是 |none|

> 返回示例

> 200 Response

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[User](#schemauser)|
|400|[Bad Request](https://tools.ietf.org/html/rfc7231#section-6.5.1)|none|[LoginResponse](#schemaloginresponse)|

# 数据模型

<h2 id="tocS_Login">Login</h2>

<a id="schemalogin"></a>
<a id="schema_Login"></a>
<a id="tocSlogin"></a>
<a id="tocslogin"></a>

```json
{
  "username": "string",
  "password": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|username|string|true|none|登录用户|none|
|password|string|true|none|用户密码|none|

<h2 id="tocS_LoginResponse">LoginResponse</h2>

<a id="schemaloginresponse"></a>
<a id="schema_LoginResponse"></a>
<a id="tocSloginresponse"></a>
<a id="tocsloginresponse"></a>

```json
{
  "message": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|message|string|true|none|错误信息|none|

<h2 id="tocS_Menu">Menu</h2>

<a id="schemamenu"></a>
<a id="schema_Menu"></a>
<a id="tocSmenu"></a>
<a id="tocsmenu"></a>

```json
{
  "id": 0,
  "children": "string",
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z",
  "parent": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|read-only||none|
|children|string|true|read-only||none|
|permission_id|integer¦null|false|none|权限id|none|
|permission_code|string¦null|false|none|权限编码|none|
|title|string|true|none|菜单标题|none|
|path|string¦null|false|none|菜单链接地址|none|
|icon|string¦null|false|none|菜单图标|none|
|sort_order|integer|false|none|菜单排序|none|
|menu_type|[MenuTypeEnum](#schemamenutypeenum)|false|none|菜单类型|* `dir` - 目录<br />* `nav` - 导航<br />* `link` - 链接<br />* `btn` - 按钮|
|update_time|string(date-time)|true|read-only|更新时间|none|
|create_time|string(date-time)|true|read-only|创建时间|none|
|parent|integer¦null|false|none|父级菜单|none|

<h2 id="tocS_MenuTypeEnum">MenuTypeEnum</h2>

<a id="schemamenutypeenum"></a>
<a id="schema_MenuTypeEnum"></a>
<a id="tocSmenutypeenum"></a>
<a id="tocsmenutypeenum"></a>

```json
"dir"

```

* `dir` - 目录
* `nav` - 导航
* `link` - 链接
* `btn` - 按钮

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|string|false|none||* `dir` - 目录<br />* `nav` - 导航<br />* `link` - 链接<br />* `btn` - 按钮|

#### 枚举值

|属性|值|
|---|---|
|*anonymous*|dir|
|*anonymous*|nav|
|*anonymous*|link|
|*anonymous*|btn|

<h2 id="tocS_PaginatedMenuList">PaginatedMenuList</h2>

<a id="schemapaginatedmenulist"></a>
<a id="schema_PaginatedMenuList"></a>
<a id="tocSpaginatedmenulist"></a>
<a id="tocspaginatedmenulist"></a>

```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "children": "string",
      "permission_id": -2147483648,
      "permission_code": "string",
      "title": "string",
      "path": "string",
      "icon": "string",
      "sort_order": -32768,
      "menu_type": "dir",
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z",
      "parent": 0
    }
  ]
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|count|integer|true|none||none|
|next|string(uri)¦null|false|none||none|
|previous|string(uri)¦null|false|none||none|
|results|[[Menu](#schemamenu)]|true|none||none|

<h2 id="tocS_PaginatedRoleList">PaginatedRoleList</h2>

<a id="schemapaginatedrolelist"></a>
<a id="schema_PaginatedRoleList"></a>
<a id="tocSpaginatedrolelist"></a>
<a id="tocspaginatedrolelist"></a>

```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "permission_ids": [
        0
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ]
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|count|integer|true|none||none|
|next|string(uri)¦null|false|none||none|
|previous|string(uri)¦null|false|none||none|
|results|[[Role](#schemarole)]|true|none||none|

<h2 id="tocS_PaginatedUserList">PaginatedUserList</h2>

<a id="schemapaginateduserlist"></a>
<a id="schema_PaginatedUserList"></a>
<a id="tocSpaginateduserlist"></a>
<a id="tocspaginateduserlist"></a>

```json
{
  "count": 123,
  "next": "http://api.example.org/accounts/?page=4",
  "previous": "http://api.example.org/accounts/?page=2",
  "results": [
    {
      "id": 0,
      "role": [
        {
          "id": 0,
          "permission": [
            {}
          ],
          "permission_ids": [
            0
          ],
          "name": "string",
          "remark": "string",
          "status": true,
          "update_time": "2019-08-24T14:15:22Z",
          "create_time": "2019-08-24T14:15:22Z"
        }
      ],
      "role_ids": [
        0
      ],
      "password": "string",
      "username": "string",
      "phone": "string",
      "email": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ]
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|count|integer|true|none||none|
|next|string(uri)¦null|false|none||none|
|previous|string(uri)¦null|false|none||none|
|results|[[User](#schemauser)]|true|none||none|

<h2 id="tocS_PatchedMenu">PatchedMenu</h2>

<a id="schemapatchedmenu"></a>
<a id="schema_PatchedMenu"></a>
<a id="tocSpatchedmenu"></a>
<a id="tocspatchedmenu"></a>

```json
{
  "id": 0,
  "children": "string",
  "permission_id": -2147483648,
  "permission_code": "string",
  "title": "string",
  "path": "string",
  "icon": "string",
  "sort_order": -32768,
  "menu_type": "dir",
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z",
  "parent": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only||none|
|children|string|false|read-only||none|
|permission_id|integer¦null|false|none|权限id|none|
|permission_code|string¦null|false|none|权限编码|none|
|title|string|false|none|菜单标题|none|
|path|string¦null|false|none|菜单链接地址|none|
|icon|string¦null|false|none|菜单图标|none|
|sort_order|integer|false|none|菜单排序|none|
|menu_type|[MenuTypeEnum](#schemamenutypeenum)|false|none|菜单类型|* `dir` - 目录<br />* `nav` - 导航<br />* `link` - 链接<br />* `btn` - 按钮|
|update_time|string(date-time)|false|read-only|更新时间|none|
|create_time|string(date-time)|false|read-only|创建时间|none|
|parent|integer¦null|false|none|父级菜单|none|

<h2 id="tocS_PatchedPermission">PatchedPermission</h2>

<a id="schemapatchedpermission"></a>
<a id="schema_PatchedPermission"></a>
<a id="tocSpatchedpermission"></a>
<a id="tocspatchedpermission"></a>

```json
{
  "id": 0,
  "children": "string",
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only||none|
|children|string|false|read-only||none|
|name|string|false|none|权限名称|none|
|code|string|false|none|权限编码|none|
|url|string¦null|false|none|接口地址|none|
|method|string¦null|false|none|接口请求方式|none|
|status|boolean|false|none|权限状态|none|
|parent|integer¦null|false|none||none|

<h2 id="tocS_PatchedRole">PatchedRole</h2>

<a id="schemapatchedrole"></a>
<a id="schema_PatchedRole"></a>
<a id="tocSpatchedrole"></a>
<a id="tocspatchedrole"></a>

```json
{
  "id": 0,
  "permission": [
    {
      "id": 0,
      "children": "string",
      "name": "string",
      "code": "string",
      "url": "string",
      "method": "string",
      "status": true,
      "parent": 0
    }
  ],
  "permission_ids": [
    0
  ],
  "name": "string",
  "remark": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only||none|
|permission|[[Permission](#schemapermission)]|false|read-only||none|
|permission_ids|[integer]|false|write-only||none|
|name|string|false|none|角色名称|none|
|remark|string|false|none|角色说明|none|
|status|boolean|false|none|角色状态,1-启用0-禁用|none|
|update_time|string(date-time)|false|read-only|更新时间|none|
|create_time|string(date-time)|false|read-only|新增时间|none|

<h2 id="tocS_PatchedUser">PatchedUser</h2>

<a id="schemapatcheduser"></a>
<a id="schema_PatchedUser"></a>
<a id="tocSpatcheduser"></a>
<a id="tocspatcheduser"></a>

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "permission_ids": [
        0
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "role_ids": [
    0
  ],
  "password": "string",
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|false|read-only||none|
|role|[[Role](#schemarole)]|false|read-only||none|
|role_ids|[integer]|false|write-only|角色id|none|
|» 角色id|integer|false|write-only|角色id|none|
|password|string|false|write-only|密码|none|
|username|string|false|none|用户名|none|
|phone|string|false|none|手机号码|none|
|email|string|false|none|邮箱地址|none|
|status|boolean|false|none|账号状态|none|
|update_time|string(date-time)|false|read-only|更新时间|none|
|create_time|string(date-time)|false|read-only|创建时间|none|

<h2 id="tocS_Permission">Permission</h2>

<a id="schemapermission"></a>
<a id="schema_Permission"></a>
<a id="tocSpermission"></a>
<a id="tocspermission"></a>

```json
{
  "id": 0,
  "children": "string",
  "name": "string",
  "code": "string",
  "url": "string",
  "method": "string",
  "status": true,
  "parent": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|read-only||none|
|children|string|true|read-only||none|
|name|string|true|none|权限名称|none|
|code|string|true|none|权限编码|none|
|url|string¦null|false|none|接口地址|none|
|method|string¦null|false|none|接口请求方式|none|
|status|boolean|false|none|权限状态|none|
|parent|integer¦null|false|none||none|

<h2 id="tocS_Role">Role</h2>

<a id="schemarole"></a>
<a id="schema_Role"></a>
<a id="tocSrole"></a>
<a id="tocsrole"></a>

```json
{
  "id": 0,
  "permission": [
    {
      "id": 0,
      "children": "string",
      "name": "string",
      "code": "string",
      "url": "string",
      "method": "string",
      "status": true,
      "parent": 0
    }
  ],
  "permission_ids": [
    0
  ],
  "name": "string",
  "remark": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|read-only||none|
|permission|[[Permission](#schemapermission)]|true|read-only||none|
|permission_ids|[integer]|true|write-only||none|
|name|string|true|none|角色名称|none|
|remark|string|true|none|角色说明|none|
|status|boolean|false|none|角色状态,1-启用0-禁用|none|
|update_time|string(date-time)|true|read-only|更新时间|none|
|create_time|string(date-time)|true|read-only|新增时间|none|

<h2 id="tocS_User">User</h2>

<a id="schemauser"></a>
<a id="schema_User"></a>
<a id="tocSuser"></a>
<a id="tocsuser"></a>

```json
{
  "id": 0,
  "role": [
    {
      "id": 0,
      "permission": [
        {
          "id": 0,
          "children": "string",
          "name": "string",
          "code": "string",
          "url": "string",
          "method": "string",
          "status": true,
          "parent": 0
        }
      ],
      "permission_ids": [
        0
      ],
      "name": "string",
      "remark": "string",
      "status": true,
      "update_time": "2019-08-24T14:15:22Z",
      "create_time": "2019-08-24T14:15:22Z"
    }
  ],
  "role_ids": [
    0
  ],
  "password": "string",
  "username": "string",
  "phone": "string",
  "email": "string",
  "status": true,
  "update_time": "2019-08-24T14:15:22Z",
  "create_time": "2019-08-24T14:15:22Z"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer|true|read-only||none|
|role|[[Role](#schemarole)]|true|read-only||none|
|role_ids|[integer]|true|write-only|角色id|none|
|» 角色id|integer|false|write-only|角色id|none|
|password|string|true|write-only|密码|none|
|username|string|true|none|用户名|none|
|phone|string|true|none|手机号码|none|
|email|string|true|none|邮箱地址|none|
|status|boolean|false|none|账号状态|none|
|update_time|string(date-time)|true|read-only|更新时间|none|
|create_time|string(date-time)|true|read-only|创建时间|none|

