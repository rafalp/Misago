import classnames from "classnames"
import React from "react"

interface ICardAlertProps {
  appearance?:
    | "primary"
    | "secondary"
    | "success"
    | "danger"
    | "warning"
    | "info"
  className?: string
  children: React.ReactNode
}

const CardAlert: React.FC<ICardAlertProps> = ({
  appearance = "danger",
  children,
  className,
}) => (
  <div
    className={classnames(
      "modal-alert",
      `modal-alert-${appearance}`,
      className
    )}
  >
    <div
      className={classnames("alert", `alert-${appearance}`, className)}
      role="alert"
    >
      {children}
    </div>
  </div>
)

export default CardAlert
