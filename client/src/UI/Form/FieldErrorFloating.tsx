import { t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import classnames from "classnames"
import React from "react"

interface IFieldErrorFloatingProps {
  type: string
  children: React.ReactNode
}

const FieldErrorFloating: React.FC<IFieldErrorFloatingProps> = ({
  type,
  children,
}) => {
  const { i18n } = useLingui()
  const [show, setShow] = React.useState(true)

  React.useEffect(() => {
    setShow(true)
  }, [type, setShow])

  return (
    <div className={classnames("invalid-feedback-floating", { show })}>
      <div>{children}</div>
      <button
        type="button"
        className="ml-2 close"
        aria-label={i18n._("close", t`Close`)}
        onClick={() => setShow(false)}
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  )
}

export default FieldErrorFloating
