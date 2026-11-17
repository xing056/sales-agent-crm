/**
 * 金额工具：全程用「整数分」计算，绝不经过浮点。
 *
 * 为什么不用 Number：
 *   后端已经把金额输出成字符串 "12800.00"，一旦 Number() 就退回二进制浮点，
 *   0.1 + 0.2 会变成 0.30000000000000004。前端虽然只做展示和汇总，
 *   但汇总就是累加，累加就会漂。
 *
 * 做法：把 "12800.00" 拆成整数部分和小数部分，拼成 BigInt 的「分」，
 * 加减全在整数域完成，最后再拼回字符串。全程无浮点，位数再多也不会错。
 */

export function toCents(value) {
  const raw = String(value ?? '0').trim()
  if (!raw || raw === 'null' || raw === 'undefined') return 0n
  const negative = raw.startsWith('-')
  const body = negative ? raw.slice(1) : raw
  const [intPart = '0', decPart = ''] = body.split('.')
  const digits = (intPart || '0') + (decPart + '00').slice(0, 2)
  const cents = BigInt(digits.replace(/^0+(?=\d)/, '') || '0')
  return negative ? -cents : cents
}

export function formatCents(cents) {
  const negative = cents < 0n
  const abs = negative ? -cents : cents
  const padded = abs.toString().padStart(3, '0')
  const intPart = padded.slice(0, -2)
  const decPart = padded.slice(-2)
  const grouped = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
  return `${negative ? '-' : ''}¥${grouped}.${decPart}`
}

/** 金额字符串/数字 → "¥12,800.00" */
export function formatMoney(value) {
  return formatCents(toCents(value))
}

/** 一组金额求和 → BigInt 分 */
export function sumCents(values) {
  return values.reduce((acc, v) => acc + toCents(v), 0n)
}
