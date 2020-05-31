import React from "react"

interface IToastsContainerProps {
  children: React.ReactNode
}

const ToastsContainer: React.FC<IToastsContainerProps> = ({ children }) => (
  <div className="toasts-container" aria-live="polite" aria-atomic="true">
    {children}
  </div>
)

export default ToastsContainer
