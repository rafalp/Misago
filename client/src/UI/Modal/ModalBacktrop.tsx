import classNames from "classnames"
import React from "react"

interface IModalBacktropProps {
  fade: boolean
  onClick?: () => void | null
}

const ModalBacktrop: React.FC<IModalBacktropProps> = ({ fade, onClick }) => (
  <div
    className={classNames("modal-backdrop", "fade", { show: fade })}
    onClick={onClick || undefined}
  />
)

export default ModalBacktrop
