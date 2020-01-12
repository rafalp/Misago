import React from "react"

export interface IValidationError {
  message: React.ReactNode
  type: string
}

export interface IValidationErrorProps {
  children: (error: IValidationError) => React.ReactElement
  error?: string | null
  value?: number
  max?: number
  min?: number
  messages?: {
    [type: string]: React.ReactNode
  } | null
}