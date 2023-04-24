import React from "react"

export default function NavbarBranding({ logo, logoXs, text, url }) {
  return (
    <div className="navbar-branding">
      {logo ? (
        <a href={url} className="navbar-branding-logo">
          <img src={logo} alt={text} />
        </a>
      ) : (
        <a href={url} className="navbar-branding-text">
          {text}
        </a>
      )}
    </div>
  )
}
