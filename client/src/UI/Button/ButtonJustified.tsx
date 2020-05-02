import classNames from "classnames"
import React from "react"

interface IButtonJustifiedProps {
  className?: string | null
  disabled?: boolean
  left?: React.ReactNode
  right?: React.ReactNode
  center?: React.ReactNode
  responsive?: boolean
  small?: boolean
  onClick?: () => void
}

const ButtonJustified: React.FC<IButtonJustifiedProps> = ({
  className,
  disabled,
  left,
  right,
  center,
  responsive,
  small,
  onClick,
}) => (
  <button
    className={classNames(
      "btn btn-secondary btn-block btn-justified",
      className,
      {
        "btn-responsive": responsive,
        "btn-sm": small,
      }
    )}
    disabled={disabled}
    type="button"
    onClick={onClick}
  >
    {left && <span className="btn-justified-left">{left}</span>}
    {center && <span className="btn-justified-center">{center}</span>}
    {right && <span className="btn-justified-right">{right}</span>}
  </button>
)

export default ButtonJustified
