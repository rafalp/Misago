let map = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#039;'
};

export default function escapeHtml(text) {
  return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}