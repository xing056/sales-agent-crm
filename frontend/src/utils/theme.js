/**
 * 明暗主题切换。
 *
 * Element Plus 官方的暗色方案就是给 <html> 加 class="dark"，
 * 配套的 CSS 变量表（theme-chalk/dark/css-vars.css）会自动接管所有 el-* 组件。
 * 我们只需要：管好这个 class + 记住用户的选择。
 *
 * 三种状态：
 *   'auto'  跟随系统（默认，用户没点过按钮时用这个）
 *   'light' 用户手动选了明亮
 *   'dark'  用户手动选了暗黑
 *
 * 为什么默认不是 light：
 *   系统已经是暗色的用户，第一次打开却被白屏糊一下，很廉价。
 *   跟随系统 + 记得手动选择，是后台管理里体验最省心的组合。
 */

const STORAGE_KEY = 'crm-theme'
const media = typeof window !== 'undefined' && window.matchMedia
  ? window.matchMedia('(prefers-color-scheme: dark)')
  : null

/** 用户的选择（可能是 'auto'） */
export function getChoice() {
  const saved = localStorage.getItem(STORAGE_KEY)
  return saved === 'light' || saved === 'dark' ? saved : 'auto'
}

/** 解析成实际生效的主题：'light' | 'dark'（兼容旧调用） */
export function getTheme() {
  const choice = getChoice()
  if (choice !== 'auto') return choice
  return media && media.matches ? 'dark' : 'light'
}

/** 把主题落到 DOM 上。animate=true 时加个短过渡，切换不突兀。 */
function paint(isDark, animate = false) {
  const root = document.documentElement
  if (animate) {
    root.classList.add('theme-transition')
    // 过渡只需要覆盖"切换的那一下"，之后摘掉，避免影响正常交互
    window.setTimeout(() => root.classList.remove('theme-transition'), 260)
  }
  root.classList.toggle('dark', isDark)
  // 让原生控件（滚动条、输入框、日期选择器的系统弹层）跟着变
  root.style.colorScheme = isDark ? 'dark' : 'light'
}

/** 直接指定主题并持久化（'light' | 'dark'），返回实际生效值 */
export function applyTheme(choice = 'light', animate = false) {
  const normalized = choice === 'dark' ? 'dark' : 'light'
  localStorage.setItem(STORAGE_KEY, normalized)
  paint(normalized === 'dark', animate)
  return normalized
}

/** 回到跟随系统 */
export function useSystemTheme() {
  localStorage.setItem(STORAGE_KEY, 'auto')
  paint(getTheme() === 'dark', true)
  return getTheme()
}

/** 在明亮/暗黑之间一键切换，返回切换后的主题 */
export function toggleTheme() {
  const next = getTheme() === 'dark' ? 'light' : 'dark'
  return applyTheme(next, true)
}

/**
 * 在 app.mount 之前调用：
 *   · 先把 class 打上，避免首屏闪白
 *   · 如果用户选的是 auto，系统主题变了要跟着变
 */
export function initTheme() {
  paint(getTheme() === 'dark', false)

  if (media) {
    const onChange = (e) => {
      // 只有"跟随系统"模式才响应；用户手动选过就尊重用户
      if (getChoice() === 'auto') paint(e.matches, true)
    }
    if (media.addEventListener) media.addEventListener('change', onChange)
    else if (media.addListener) media.addListener(onChange) // 老 Safari
  }
}
