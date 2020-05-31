import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import classNames from "classnames"
import React from "react"

interface IToastProps {
  text: React.ReactNode
  show?: boolean
  remove: () => void
}

enum ToastState {
  NEW = 0,
  SHOW = 1,
  HIDE = 2,
}

const TOAST_LIFETIME = 7000
const TOAST_REMOVE_DELAY = 300

const Toast: React.FC<IToastProps> = ({ show, text, remove }) => {
  const [state, setState] = React.useState<ToastState>(
    show ? ToastState.SHOW : ToastState.NEW
  )

  React.useEffect(() => {
    // Note: we don't cleanup timeouts because it required
    // memoization of "remove" for animation to still work
    if (state === ToastState.NEW) {
      window.setTimeout(() => setState(ToastState.SHOW), 100)
    }
    if (state === ToastState.SHOW) {
      window.setTimeout(() => setState(ToastState.HIDE), TOAST_LIFETIME)
    }
    if (state === ToastState.HIDE) {
      window.setTimeout(() => remove(), TOAST_REMOVE_DELAY)
    }
  }, [state, remove])

  return (
    <div
      className={classNames("toast", {
        fade: state !== ToastState.NEW,
        show: state === ToastState.SHOW,
      })}
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div className="toast-body">
        <div>{text}</div>
        <I18n>
          {({ i18n }) => (
            <button
              type="button"
              className="ml-2 close"
              data-dismiss="toast"
              aria-label={i18n._(t("close")`Close`)}
              onClick={() => {
                setState(ToastState.HIDE)
              }}
            >
              <span aria-hidden="true">&times;</span>
            </button>
          )}
        </I18n>
      </div>
    </div>
  )
}

export default Toast
