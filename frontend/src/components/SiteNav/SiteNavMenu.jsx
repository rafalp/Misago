import classnames from "classnames"
import React from "react"
import { connect } from "react-redux"
import {
  DropdownDivider,
  DropdownHeader,
  DropdownMenuItem,
  DropdownPills,
  DropdownSubheader,
} from "../Dropdown"
import RegisterButton from "../RegisterButton"
import SignInButton from "../SignInButton"

function SiteNavMenu({ isAnonymous, close, dropdown, overlay }) {
  const baseUrl = misago.get("MISAGO_PATH")
  const settings = misago.get("SETTINGS")
  const mainItems = misago.get("main_menu")
  const extraItems = misago.get("extraMenuItems")
  const extraFooterItems = misago.get("extraFooterItems")
  const categories = misago.get("categories_menu")
  const users = misago.get("usersLists")
  const authDelegated = settings.enable_oauth2_client

  const topNav = []
  mainItems.forEach((item) => {
    topNav.push({ title: item.label, url: item.url })
  })

  topNav.push({
    title: pgettext("site nav", "Search"),
    url: baseUrl + "search/",
  })

  const footerNav = []

  const tosTitle = misago.get("TERMS_OF_SERVICE_TITLE")
  const tosUrl = misago.get("TERMS_OF_SERVICE_URL")
  if (tosTitle && tosUrl) {
    footerNav.push({
      title: tosTitle,
      url: tosUrl,
    })
  }

  const privacyTitle = misago.get("PRIVACY_POLICY_TITLE")
  const privacyUrl = misago.get("PRIVACY_POLICY_URL")
  if (privacyTitle && privacyUrl) {
    footerNav.push({
      title: privacyTitle,
      url: privacyUrl,
    })
  }

  return (
    <ul
      className={classnames("site-nav-menu", {
        "dropdown-menu-list": dropdown,
        "overlay-menu-list": overlay,
      })}
    >
      {isAnonymous && (
        <DropdownHeader className="site-nav-sign-in-message">
          {pgettext("cta", "You are not signed in")}
        </DropdownHeader>
      )}
      {isAnonymous && (
        <DropdownPills className="site-nav-sign-in-options">
          <SignInButton onClick={close} />
          {!authDelegated && <RegisterButton onClick={close} />}
        </DropdownPills>
      )}
      <DropdownSubheader>{settings.forum_name}</DropdownSubheader>
      {topNav.map((item) => (
        <DropdownMenuItem key={item.url}>
          <a href={item.url}>{item.title}</a>
        </DropdownMenuItem>
      ))}
      {extraItems.map((item, index) => (
        <DropdownMenuItem key={index} className={item.className}>
          <a
            href={item.url}
            target={item.targetBlank ? "_blank" : null}
            rel={item.rel}
          >
            {item.title}
          </a>
        </DropdownMenuItem>
      ))}
      {!!users.length && <DropdownDivider className="site-nav-users-divider" />}
      {!!users.length && (
        <DropdownSubheader className="site-nav-users">
          {pgettext("site nav section", "Users")}
        </DropdownSubheader>
      )}
      {users.map((item) => (
        <DropdownMenuItem key={item.url}>
          <a href={item.url}>{item.name}</a>
        </DropdownMenuItem>
      ))}
      <DropdownDivider className="site-nav-categories-divider" />
      <DropdownSubheader className="site-nav-categories">
        {pgettext("site nav section", "Categories")}
      </DropdownSubheader>
      {categories.map((category) =>
        category.is_vanilla ? (
          <DropdownMenuItem
            className="site-nav-category-header"
            key={category.id}
          >
            <a href={category.url}>{category.name}</a>
          </DropdownMenuItem>
        ) : (
          <DropdownMenuItem
            className={classnames("site-nav-category", {
              "site-nav-category-last": category.last,
            })}
            key={category.id}
          >
            <a href={category.url}>
              <span>{category.name}</span>
              <span
                className={classnames(
                  "threads-list-item-category threads-list-category-label",
                  { "threads-list-category-label-color": !!category.color }
                )}
                style={{ "--label-color": category.color }}
              >
                {category.short_name || category.name}
              </span>
            </a>
          </DropdownMenuItem>
        )
      )}
      {(!!footerNav.length || !!extraFooterItems.length) && (
        <DropdownDivider className="site-nav-footer-divider" />
      )}
      {(!!footerNav.length || !!extraFooterItems.length) && (
        <DropdownSubheader className="site-nav-footer">
          {pgettext("site nav section", "Footer")}
        </DropdownSubheader>
      )}
      {extraFooterItems.map((item, index) => (
        <DropdownMenuItem key={index} className={item.className}>
          <a
            href={item.url}
            target={item.targetBlank ? "_blank" : null}
            rel={item.rel}
          >
            {item.title}
          </a>
        </DropdownMenuItem>
      ))}
      {footerNav.map((item) => (
        <DropdownMenuItem key={item.url}>
          <a href={item.url}>{item.title}</a>
        </DropdownMenuItem>
      ))}
    </ul>
  )
}

function select(state) {
  return {
    isAnonymous: !state.auth.user.id,
  }
}

const SiteNavMenuConnected = connect(select)(SiteNavMenu)

export default SiteNavMenuConnected
