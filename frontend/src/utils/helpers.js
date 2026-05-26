// Format price to Indian Rupee string
export function formatPrice(amount) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 2
  }).format(amount)
}

//  date to readable string
export function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric'
  })
}

// debounce function  
export function debounce(fn, delay = 400) {
  let timer
  return function (...args) {
    clearTimeout(timer)
    timer = setTimeout(() => fn.apply(this, args), delay)
  }
}

// Truncate long text
export function truncate(text, length = 60) {
  if (!text) return ''
  return text.length > length ? text.slice(0, length) + '…' : text
}