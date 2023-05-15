import classnames from "classnames"
import React from "react"
import modal from "../../services/modal"
import SignInModal from "../sign-in"

export default function SignInButton({ block, className, onClick }) {
  const settings = misago.get("SETTINGS")

  if (settings.DELEGATE_AUTH) {
    return (
      <a
        className={classnames("btn btn-sign-in", className, {
          "btn-block": block,
        })}
        href={settings.LOGIN_URL}
        onClick={onClick}
      >
        {pgettext("cta", "Sign in")}
      </a>
    )
  }

  return (
    <button
      className={classnames("btn btn-sign-in", className, {
        "btn-block": block,
      })}
      type="button"
      onClick={() => {
        if (onClick) {
          onClick()
        }

        modal.show(<SignInModal />)
      }}
    >
      {pgettext("cta", "Sign in")}
    </button>
  )
}
