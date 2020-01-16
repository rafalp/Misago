import classNames from "classnames"
import React from "react"
import ModalBacktrop from "./ModalBacktrop"
import useTransition from "./useTransition"

interface IModalProps {
  children: React.ReactNode
  isOpen: boolean
  resistant?: boolean
  close: () => void
}

const Modal: React.FC<IModalProps> = ({
  children,
  isOpen,
  resistant = false,
  close,
}) => {
  const { display, fade } = useTransition(isOpen)
  if (!display) return null

  return (
    <div onClick={resistant ? undefined : close}>
      <div
        className={classNames("modal", "d-block", "fade", { show: fade })}
        tabIndex={-1}
        role="dialog"
        aria-hidden={fade ? "false" : "true"}
        onKeyDown={({ keyCode }) => {
          if (keyCode === 27) close()
        }}
      >
        {children}
      </div>
      <ModalBacktrop fade={fade} onClick={resistant ? undefined : close} />
    </div>
  )
}

export default Modal
