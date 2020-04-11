import classNames from "classnames"
import React from "react"

interface ICardErrorProps {
  className?: string | null
  header: React.ReactNode | null
  message?: React.ReactNode | null
}

const CardError: React.FC<ICardErrorProps> = ({
  className,
  header,
  message,
}) => (
  <div className={classNames("card-body card-error", className)}>
    <div className={"card-error-body"}>
      <div className={"card-error-icon"} />
      <div className={"card-error-message"}>
        <h3>{header}</h3>
        {message && <p>{message}</p>}
      </div>
    </div>
  </div>
)

export default CardError
