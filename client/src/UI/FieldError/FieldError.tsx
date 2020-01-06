import React from "react"

interface IFieldErrorProps {
  error?: string | null
  messages: {
    [type: string]: React.ReactNode
  }
}

const FieldError: React.FC<IFieldErrorProps> = ({ error, messages }) => {
  if (!error) return null
  return <div>{messages[error] || error}</div>
}

export default FieldError
