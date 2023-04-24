export const OPEN_SITE_NAV = "OPEN_SITE_NAV"
export const OPEN_SEARCH = "OPEN_SEARCH"
export const OPEN_NOTIFICATIONS = "OPEN_NOTIFICATIONS"
export const OPEN_PRIVATE_THREADS = "OPEN_PRIVATE_THREADS"
export const OPEN_USER_NAV = "OPEN_USER_NAV"
export const CLOSE = "CLOSE_OVERLAYS"

export function openSiteNav() {
  return { type: OPEN_SITE_NAV }
}

export function openSearch() {
  return { type: OPEN_SEARCH }
}

export function openNotifications() {
  return { type: OPEN_NOTIFICATIONS }
}

export function openPrivateThreads() {
  return { type: OPEN_PRIVATE_THREADS }
}

export function openUserNav() {
  return { type: OPEN_USER_NAV }
}

export function close() {
  return { type: CLOSE }
}

export const initialState = {
  siteNav: false,
  search: false,
  notifications: false,
  privateThreads: false,
  userNav: false,
}

export default function notifications(state = initialState, action = null) {
  switch (action.type) {
    case OPEN_SITE_NAV:
      return Object.assign({}, state, initialState, { siteNav: true })

    case OPEN_SEARCH:
      return Object.assign({}, state, initialState, { search: true })

    case OPEN_NOTIFICATIONS:
      return Object.assign({}, state, initialState, { notifications: true })

    case OPEN_PRIVATE_THREADS:
      return Object.assign({}, state, initialState, { privateThreads: true })

    case OPEN_USER_NAV:
      return Object.assign({}, state, initialState, { userNav: true })

    case CLOSE:
      return Object.assign({}, state, initialState)

    default:
      return state
  }
}
