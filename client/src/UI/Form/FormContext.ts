import React from "react"

interface FormContextData {
  id?: string
  disabled?: boolean
}

const FormContext = React.createContext<FormContextData>({})

const useFormContext = () => React.useContext(FormContext)

export { FormContext, useFormContext }
