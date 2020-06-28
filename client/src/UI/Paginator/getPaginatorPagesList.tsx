const getPaginatorPagesList = (page: number, pages: number) => {
  const list: Array<number | null> = []
  if (page > 3) {
    list.push(1)
    if (page > 4) {
      list.push(null)
    }
  }

  const start = page > 3 ? page - 2 : 1
  const end = page + 3 > pages ? pages : page + 2
  for (let i = start; i <= end; i++) {
    list.push(i)
  }

  if (page + 2 < pages) {
    if (page + 4 === pages) {
      list.push(page + 3)
    } else if (page + 3 < pages) {
      list.push(null)
    }
    list.push(pages)
  }
  return list
}

export default getPaginatorPagesList
