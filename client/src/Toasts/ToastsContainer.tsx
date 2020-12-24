import React from "react"

interface ToastsContainerProps {
  children: React.ReactNode
}

const ToastsContainer: React.FC<ToastsContainerProps> = ({ children }) => (
  <div className="toasts-container" aria-live="polite" aria-atomic="true">
    {children}
  </div>
)

export default ToastsContainer
