import React from "react"

export interface ButtonProps {
  block?: boolean
  className?: string | null
  disabled?: boolean
  elementRef?: React.MutableRefObject<HTMLButtonElement | null>
  icon?: string
  image?: React.ReactNode
  loading?: boolean
  responsive?: boolean
  small?: boolean
  text?: React.ReactNode
  outline?: boolean
  onClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void
}
