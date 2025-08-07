import { httpResponseError } from "../snackbars"

class SourceUsers {
  constructor() {
    this.cache = {}
    this.url = window.misago_suggest_users
  }

  get = ({ value, exclude }, showErrors) => {
    let url = this.url + "?query=" + encodeURIComponent(value)
    if (exclude && Array.isArray(exclude)) {
      exclude.forEach(function (item) {
        if (item) {
          url += "&exclude=" + encodeURIComponent(item)
        }
      })
    }

    if (this.cache[url]) {
      return Promise.resolve(this.cache[url])
    }

    return fetch(url).then(
      async (response) => {
        if (!response.ok) {
          if (showErrors) {
            httpResponseError(response)
          }
          console.error(response)
          return []
        }

        const { results } = await response.json()
        this.cache[url] = results
        return results
      },
      () => {
        return []
      }
    )
  }
}

const _users = new SourceUsers()

function users(query, showErrors) {
  return _users.get(query, showErrors)
}

export { users }
