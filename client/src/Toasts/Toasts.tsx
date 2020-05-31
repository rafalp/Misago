import React from "react"
import { useToastsContext } from "../Context"
import Toast from "./Toast"
import ToastsContainer from "./ToastsContainer"

const Toasts: React.FC = () => {
  const { toasts, removeToast } = useToastsContext()

  return (
    <ToastsContainer>
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          text={toast.text}
          remove={() => removeToast(toast.id)}
        />
      ))}
    </ToastsContainer>
  )
}

export default Toasts
