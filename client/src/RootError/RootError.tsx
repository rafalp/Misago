import classNames from "classnames"
import React from "react"

interface IRootErrorProps {
  className?: string
  icon: React.ReactNode
  message: string
  help: string
}

const RootError: React.FC<IRootErrorProps> = ({ className, icon, help, message }) => (
  <div className={classNames("root-error", className)}>
    <div className="root-error-body">
      <div className="root-error-icon">{icon}</div>
      <div className="root-error-message">
        <h1>{message}</h1>
        <p>{help}</p>
      </div>
    </div>
  </div>
)

export default RootError
