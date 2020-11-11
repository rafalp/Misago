import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import classnames from "classnames"
import React from "react"

interface IFieldErrorFloatingProps {
  type: string
  children: React.ReactNode
}

const FieldErrorFloating: React.FC<IFieldErrorFloatingProps> = ({
  type, children,
}) => {
  const [visible, setVisible] = React.useState(true)

  React.useEffect(() => {
    setVisible(true)
  }, [type, setVisible])

  return (
    <div className={classnames("invalid-feedback-floating", { visible })}>
      <div>{children}</div>
      <I18n>
        {({ i18n }) => (
          <button
            type="button"
            className="ml-2 close"
            aria-label={i18n._(t("close")`Close`)}
            onClick={() => setVisible(false)}
          >
            <span aria-hidden="true">&times;</span>
          </button>
        )}
      </I18n>
    </div>
  )
}

export default FieldErrorFloating
