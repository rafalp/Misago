import React from "react"

type Error = {
  message: React.ReactNode
  type: string
}

export interface ValidationErrorProps {
  children: (error: Error) => React.ReactElement
  error?: Error | null
  value?: number
  max?: number
  min?: number
  messages?: {
    [type: string]: React.ReactNode
  } | null
}
