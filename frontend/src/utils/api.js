import http from './http'
// 请求登录接口
// payload={username,password}
export const login = (payload) => http.post('/user/login/', payload)
// 请求权限列表
export const getPermList = () => http.get('/permission/')
// 新增权限数据 payload={name,code,status,parent}
export const createPerm = (payload) => http.post('/permission/', payload)
// 更新权限数据 payload={name,code,status,parent}
export const updatePerm = (id, payload) => http.patch(`/permission/${id}/`, payload)
// 删除权限数据 payload={name,code,status,parent}
export const removePerm = (id) => http.delete(`/permission/${id}/`)


// 请求角色列表 params={page}
export const getRoleList = (params) => http.get('/role/', { params })
// 新增角色数据 payload={name,code,status,parent}
export const createRole = (payload) => http.post('/role/', payload)
// 更新角色数据 payload={name,code,status,parent}
export const updateRole = (id, payload) => http.patch(`/role/${id}/`, payload)
// 删除角色数据 payload={name,code,status,parent}
export const removeRole = (id) => http.delete(`/role/${id}/`)

// 请求菜单列表 params={page}
export const getMenuList = (params) => http.get('/menu/', { params })
// 新增菜单数据 payload={name,code,status,parent}
export const createMenu = (payload) => http.post('/menu/', payload)
// 更新菜单数据 payload={name,code,status,parent}
export const updateMenu = (id, payload) => http.patch(`/menu/${id}/`, payload)
// 删除菜单数据 payload={name,code,status,parent}
export const removeMenu = (id) => http.delete(`/menu/${id}/`)

// 请求用户列表 params={page}
export const getUserList = (params) => http.get('/user/', { params })
// 新增用户数据 payload={name,code,status,parent}
export const createUser = (payload) => http.post('/user/', payload)
// 更新用户数据 payload={name,code,status,parent}
export const updateUser = (id, payload) => http.patch(`/user/${id}/`, payload)
// 删除用户数据 payload={name,code,status,parent}
export const removeUser = (id) => http.delete(`/user/${id}/`)


// 请求部门列表 params={page}
export const getDepartmentList = (params) => http.get('/department/', { params })
// 新增部门数据 payload={name,code,status,parent}
export const createDepartment = (payload) => http.post('/department/', payload)
// 更新部门数据 payload={name,code,status,parent}
export const updateDepartment = (id, payload) => http.patch(`/department/${id}/`, payload)
// 删除部门数据 payload={name,code,status,parent}
export const removeDepartment = (id) => http.delete(`/department/${id}/`)
// 查询部门详情数据
export const getDepartment = (id) => http.get(`/department/${id}/`)



// 请求职位列表 params={page}
export const getPositionList = (params = {}) => http.get('/position/', { params })
// 新增职位数据 payload={name,code,status,parent}
export const createPosition = (payload) => http.post('/position/', payload)
// 更新职位数据 payload={name,code,status,parent}
export const updatePosition = (id, payload) => http.patch(`/position/${id}/`, payload)
// 删除职位数据 payload={name,code,status,parent}
export const removePosition = (id) => http.delete(`/position/${id}/`)



// 请求员工列表 params={page}
export const getEmployeeList = (params = {}) => http.get('/employee/', { params })
// 新增员工数据 payload={name,code,status,parent}
export const createEmployee = (payload) => http.post('/employee/', payload)
// 更新员工数据 payload={name,code,status,parent}
export const updateEmployee = (id, payload) => http.patch(`/employee/${id}/`, payload)
// 删除员工数据 payload={name,code,status,parent}
export const removeEmployee = (id) => http.delete(`/employee/${id}/`)
// 获取员工详情数据
export const getEmployee = (id) => http.get(`/employee/${id}/`)
// 导出员工列表数据
// responseType: 数据接口返回的数据类型
// params={department_id:1}
export const downloadEmployee = (params = {}) => http.get('/employee/download/', { params, responseType: 'blob' })


// 获取中文对应的汉语拼音
export const getSpell = (words) => http.get(`/common/get_spell/`, { params: { words } })


// 请求客户来源列表 params={page}
export const getCustomerSourceList = (params = {}) => http.get('/customer_source/', { params })
// 新增客户来源数据 payload={name,code,status,parent}
export const createCustomerSource = (payload) => http.post('/customer_source/', payload)
// 更新客户来源数据 payload={name,code,status,parent}
export const updateCustomerSource = (id, payload) => http.patch(`/customer_source/${id}/`, payload)
// 删除客户来源数据 payload={name,code,status,parent}
export const removeCustomerSource = (id) => http.delete(`/customer_source/${id}/`)


// 请求客户列表 params={page}
export const getCustomerList = (params = {}) => http.get('/customer/', { params })
// 新增客户数据 payload={name,code,status,parent}
export const createCustomer = (payload) => http.post('/customer/', payload)
// 更新客户数据 payload={name,code,status,parent}
export const updateCustomer = (id, payload) => http.patch(`/customer/${id}/`, payload)
// 删除客户数据 payload={name,code,status,parent}
export const removeCustomer = (id) => http.delete(`/customer/${id}/`)
// 请求客户详情
export const getCustomer = (id) => http.get(`/customer/${id}/`)
// 请求当前登录账号对应的客户列表数据
export const getCustomerListOfMe = (params = {}) => http.get(`/customer/of_me/`, { params })



// 请求客户跟踪记录列表 params={page}
export const getCustomerTrackingList = (params = {}) => http.get('/customer_tracking/', { params })
// 新增客户跟踪记录数据 payload={name,code,status,parent}
export const createCustomerTracking = (payload) => http.post('/customer_tracking/', payload)
// 更新客户跟踪记录数据 payload={name,code,status,parent}
export const updateCustomerTracking = (id, payload) => http.patch(`/customer_tracking/${id}/`, payload)
// 删除客户跟踪记录数据 payload={name,code,status,parent}
export const removeCustomerTracking = (id) => http.delete(`/customer_tracking/${id}/`)
// 请求客户跟踪记录详情
export const getCustomerTracking = (id) => http.get(`/customer_tracking/${id}/`)



// 请求商品分类列表 params={page}
export const getCategoryList = (params = {}) => http.get('/category/', { params })
// 新增商品分类数据 payload={name,code,status,parent}
export const createCategory = (payload) => http.post('/category/', payload)
// 更新商品分类数据 payload={name,code,status,parent}
export const updateCategory = (id, payload) => http.patch(`/category/${id}/`, payload)
// 删除商品分类数据 payload={name,code,status,parent}
export const removeCategory = (id) => http.delete(`/category/${id}/`)
// 请求商品分类详情
export const getCategory = (id) => http.get(`/category/${id}/`)


// 请求商品列表 params={page}
export const getProductList = (params = {}) => http.get('/product/', { params })
// 新增商品数据 payload={name,code,status,parent}
export const createProduct = (payload) => http.post('/product/', payload)
// 更新商品数据 payload={name,code,status,parent}
export const updateProduct = (id, payload) => http.patch(`/product/${id}/`, payload)
// 删除商品数据 payload={name,code,status,parent}
export const removeProduct = (id) => http.delete(`/product/${id}/`)
// 请求商品详情
export const getProduct = (id) => http.get(`/product/${id}/`)


// 请求销售订单列表 params={page}
export const getSaleOrderList = (params = {}) => http.get('/sale_order/', { params })
// 新增销售订单数据 payload={name,code,status,parent}
export const createSaleOrder = (payload) => http.post('/sale_order/', payload)
// 更新销售订单数据 payload={name,code,status,parent}
export const updateSaleOrder = (id, payload) => http.patch(`/sale_order/${id}/`, payload)
// 删除销售订单数据 payload={name,code,status,parent}
export const removeSaleOrder = (id) => http.delete(`/sale_order/${id}/`)
// 请求销售订单详情
export const getSaleOrder = (id) => http.get(`/sale_order/${id}/`)
// 请求订单商品列表
export const getSaleOrderProductList = (order_id) => http.get('/sale_order_item/', { params: { order_id } })


// 请求销量前10名的商品销售数据
export const getTopSaleProduct = () => http.get('/stat/top_sale_product/')
// 请求销售额前10的销售人员的销售数据
export const getTop10Employee = () => http.get('/stat/top10_sale_employee/')
// 请求客户数量排行前10的省份数据
export const getTop10Customer = () => http.get('/stat/top10_province_customer/')
// 请求本周每天的销售额
export const getWeekDaySaleAmount = () => http.get('/stat/weekday_sale_amount/')
// 请求本月每天的销售额
export const getMonthDaySaleAmount = () => http.get('/stat/month_day_sale_amount/')
// 请求本年度每月的销售额
export const getYearMonthSaleAmount = () => http.get('/stat/year_month_sale_amount/')


// 请求提成列表 params={page}
export const getCommissionList = (params = {}) => http.get('/commission/', { params })
// 获取我的提成列表
export const getCommissionListOfMe = (params = {}) => http.get('/commission/of_me/', { params })
// 生成提成数据
export const createCommission = (payload) => http.post('/commission/', payload)
