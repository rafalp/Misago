import React from "react"

export default function NavbarBranding({ logo, logoXs, text, url }) {
  if (logo) {
    return (
      <div className="navbar-branding">
        <a href={url} className="navbar-branding-logo">
          <img src={logo} alt={text} />
        </a>
      </div>
    )
  }

  return (
    <div className="navbar-branding">
      {!!logoXs && (
        <a href={url} className="navbar-branding-logo-xs">
          <img src={logoXs} alt={text} />
        </a>
      )}
      {!!text && (
        <a href={url} className="navbar-branding-text">
          {text}
        </a>
      )}
    </div>
  )
}
