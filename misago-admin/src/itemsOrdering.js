import Sortable from 'sortablejs'

export default function initItemsOrdering(url) {
  const tbody = document.querySelector(".card-admin-table tbody")
  const sortable = new Sortable(
    tbody,
    {
      animation: 150,
      handle: ".btn-handle",
      dataIdAttr: "data-item-id",

      onEnd: () => {
        const data = new URLSearchParams()
        data.append("csrfmiddlewaretoken", document.querySelector("input[name=csrfmiddlewaretoken]").value)

        sortable.toArray().forEach(item => {
          data.append("item", item)
        })

        fetch(
          url,
          {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            body: data,
          },
        )
      }
    },
  )
  return sortable
}