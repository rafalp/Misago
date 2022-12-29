export default function (list, rowWidth, padding = false) {
  let rows = []
  let row = []

  list.forEach(function (element) {
    row.push(element)
    if (row.length === rowWidth) {
      rows.push(row)
      row = []
    }
  })

  // pad row to required length?
  if (padding !== false && row.length > 0 && row.length < rowWidth) {
    for (let i = row.length; i < rowWidth; i++) {
      row.push(padding)
    }
  }

  if (row.length) {
    rows.push(row)
  }

  return rows
}
