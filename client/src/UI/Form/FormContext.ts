import React from "react"

interface FormContext {
  id?: string
  disabled?: boolean
}

const FormContext = React.createContext<FormContext>({})

const useFormContext = () => React.useContext(FormContext)

export { FormContext, useFormContext }
