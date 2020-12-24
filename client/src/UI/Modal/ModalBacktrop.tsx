import classnames from "classnames"
import React from "react"

interface ModalBacktropProps {
  fade: boolean
  onClick?: () => void | null
}

const ModalBacktrop: React.FC<ModalBacktropProps> = ({ fade, onClick }) => (
  <div
    className={classnames("modal-backdrop", "fade", { show: fade })}
    onClick={onClick || undefined}
  />
)

export default ModalBacktrop
