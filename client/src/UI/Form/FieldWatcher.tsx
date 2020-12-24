import React from "react"
import { useFormContext } from "react-hook-form"

interface FieldWatcherProps {
  name: string
  onChange: (value: string) => void
}

const FieldWatcher: React.FC<FieldWatcherProps> = ({ name, onChange }) => {
  const context = useFormContext()
  const value = context.watch(name)
  React.useEffect(() => onChange(value), [value, onChange])

  return null
}

export default FieldWatcher
