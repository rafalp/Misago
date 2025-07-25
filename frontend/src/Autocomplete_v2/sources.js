class SourceUsers {
  constructor() {
    this.cache = {}
    this.url = window.misago_suggest_users
  }

  get = (query) => {
    if (this.cache[query]) {
      return Promise.resolve(this.cache[query])
    }

    return fetch(this.url + "?query=" + encodeURIComponent(query)).then(
      async (response) => {
        if (!response.ok) {
          return []
        }

        const { results } = await response.json()
        this.cache[query] = results
        return results
      },
      () => {
        return []
      }
    )
  }
}

const _users = new SourceUsers()

function users(query) {
  return _users.get(query)
}

export { users }
