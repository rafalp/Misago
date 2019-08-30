import React from "react"
import Avatar from "misago/components/avatar"
import NavbarSearch from "misago/components/navbar-search"
import RegisterButton from "misago/components/register-button"
import SignInModal from "misago/components/sign-in.js"
import misago from "misago"
import dropdown from "misago/services/mobile-navbar-dropdown"
import modal from "misago/services/modal"

export class GuestMenu extends React.Component {
  showSignInModal() {
    modal.show(SignInModal)
  }

  render() {
    return (
      <ul
        className="dropdown-menu user-dropdown dropdown-menu-right"
        role="menu"
      >
        <li className="guest-preview">
          <h4>{gettext("You are browsing as guest.")}</h4>
          <p>
            {gettext(
              "Sign in or register to start and participate in discussions."
            )}
          </p>
          <div className="row">
            {misago.get("SETTINGS").enable_sso ? (
              <div className="col-xs-12">
                <a
                  className="btn btn-primary btn-register btn-block"
                  href={misago.get("SETTINGS").SSO_LOGIN_URL}
                >
                  {gettext("Sign in")}
                </a>
              </div>
            ) : (
              <div className="col-xs-6">
                <button
                  className="btn btn-default btn-sign-in btn-block"
                  onClick={this.showSignInModal}
                  type="button"
                >
                  {gettext("Sign in")}
                </button>
              </div>
            )}
            {!misago.get("SETTINGS").enable_sso && (
              <div className="col-xs-6">
                <RegisterButton className="btn-primary btn-register btn-block">
                  {gettext("Register")}
                </RegisterButton>
              </div>
            )}
          </div>
        </li>
      </ul>
    )
  }
}

export class GuestNav extends GuestMenu {
  render() {
    return (
      <div className="nav nav-guest">
        {misago.get("SETTINGS").enable_sso ? (
          <a
            className="btn navbar-btn btn-primary btn-register"
            href={misago.get("SETTINGS").SSO_LOGIN_URL}
          >
            {gettext("Sign in")}
          </a>
        ) : (
          <button
            className="btn navbar-btn btn-default btn-sign-in"
            onClick={this.showSignInModal}
            type="button"
          >
            {gettext("Sign in")}
          </button>
        )}
        {!misago.get("SETTINGS").enable_sso && (
          <RegisterButton className="navbar-btn btn-primary btn-register">
            {gettext("Register")}
          </RegisterButton>
        )}
        <div className="navbar-left">
          <NavbarSearch />
        </div>
      </div>
    )
  }
}

export class CompactGuestNav extends React.Component {
  showGuestMenu() {
    dropdown.show(GuestMenu)
  }

  render() {
    return (
      <button type="button" onClick={this.showGuestMenu}>
        <Avatar size="64" />
      </button>
    )
  }
}
