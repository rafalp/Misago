import React from "react"
import { connect } from "react-redux"
import * as overlay from "../../reducers/overlay"
import RegisterButton from "../RegisterButton"
import SignInButton from "../SignInButton"
import NavbarBranding from "./NavbarBranding"
import NavbarExtraMenu from "./NavbarExtraMenu"
import NavbarNotificationsToggle from "./NavbarNotificationsToggle"
import NavbarPrivateThreadsToggle from "./NavbarPrivateThreadsToggle"
import NavbarSearchToggle from "./NavbarSearchToggle"
import NavbarSiteNavDropdown from "./NavbarSiteNavDropdown"
import NavbarSiteNavToggle from "./NavbarSiteNavToggle"
import NavbarUserNavToggle from "./NavbarUserNavToggle"

export function Navbar({
  dispatch,
  branding,
  extraMenuItems,
  authDelegated,
  user,
  searchUrl,
  notificationsUrl,
  privateThreadsUrl,
  showSearch,
  showPrivateThreads,
}) {
  return (
    <div className="container navbar-container">
      <NavbarBranding {...branding} />
      <div className="navbar-right">
        {!!extraMenuItems && <NavbarExtraMenu items={extraMenuItems} />}
        {!!showSearch && (
          <NavbarSearchToggle
            id="navbar-search-overlay"
            url={searchUrl}
            onClick={(event) => {
              dispatch(overlay.openSearch())
              event.preventDefault()
            }}
          />
        )}
        <NavbarSiteNavDropdown id="navbar-site-nav-dropdown" />
        <NavbarSiteNavToggle
          id="navbar-site-nav-overlay"
          onClick={() => {
            dispatch(overlay.openSiteNav())
          }}
        />
        {!!showPrivateThreads && (
          <NavbarPrivateThreadsToggle
            id="navbar-private-threads-overlay"
            badge={user.unreadPrivateThreads}
            url={privateThreadsUrl}
            onClick={(event) => {
              dispatch(overlay.openPrivateThreads())
              event.preventDefault()
            }}
          />
        )}
        {!!user && (
          <NavbarNotificationsToggle
            id="navbar-notifications-overlay"
            badge={user.unreadNotifications}
            url={notificationsUrl}
            onClick={(event) => {
              dispatch(overlay.openNotifications())
              event.preventDefault()
            }}
          />
        )}
        {!!user && (
          <NavbarUserNavToggle
            id="navbar-user-nav-overlay"
            user={user}
            onClick={(event) => {
              dispatch(overlay.openUserNav())
              event.preventDefault()
            }}
          />
        )}
        {!user && <SignInButton className="btn-navbar-sign-in" />}
        {!user && !authDelegated && (
          <RegisterButton className="btn-navbar-register" />
        )}
      </div>
    </div>
  )
}

function select(state) {
  const settings = misago.get("SETTINGS")
  const user = state.auth.user

  return {
    branding: {
      logo: settings.logo,
      logoXs: settings.logo_small,
      text: settings.logo_text,
      url: misago.get("MISAGO_PATH"),
    },
    extraMenuItems: misago.get("extraMenuItems"),

    user: !user.id
      ? null
      : {
          id: user.id,
          username: user.username,
          email: user.email,
          avatars: user.avatars,
          unreadNotifications: user.unread_notifications,
          unreadPrivateThreads: user.unread_private_threads,
          url: user.url,
        },

    searchUrl: misago.get("SEARCH_URL"),
    notificationsUrl: misago.get("NOTIFICATIONS_URL"),
    privateThreadsUrl: misago.get("PRIVATE_THREADS_URL"),

    showSearch: !!user.acl.can_search,
    showPrivateThreads: !!user && !!user.acl.can_use_private_threads,
  }
}

const NavbarConnected = connect(select)(Navbar)

export default NavbarConnected
