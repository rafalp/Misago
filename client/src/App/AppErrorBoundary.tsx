import React from "react"
import AppError from "./AppError"

interface IAppErrorBoundaryProps {
  children: React.ReactNode
}

class AppErrorBoundary extends React.Component<IAppErrorBoundaryProps> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) return <AppError />
    return this.props.children
  }
}

export default AppErrorBoundary
