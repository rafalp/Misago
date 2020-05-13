import React from "react"
import {
  FieldValues,
  FormContext as HookFormContext,
  useForm,
} from "react-hook-form"
import { FormContext } from "./FormContext"

interface IOnSubmit<FormValues> {
  data: FormValues
  event?: React.BaseSyntheticEvent<object, any, any>
  clearError: (name?: string | string[]) => void
  setError: (name: string, type: string, message?: string) => void
}

interface IFormProps<FormValues> {
  children?: React.ReactNode
  defaultValues?: FormValues
  disabled?: boolean
  id?: string
  onSubmit?: (args: IOnSubmit<FormValues>) => void | Promise<void>
  validationMode?: "onSubmit" | "onBlur" | "onChange"
  validationSchema?: any
}

const Form = <
  FormValues extends FieldValues = FieldValues,
  ValidationContext extends object = object
>(
  props: IFormProps<FormValues>
): JSX.Element => {
  const {
    children,
    defaultValues,
    disabled,
    id,
    onSubmit,
    validationMode,
    validationSchema,
  } = props
  const methods = useForm<FormValues, ValidationContext>({
    defaultValues,
    validationSchema,
    mode: validationMode || "onBlur",
  })

  return (
    <HookFormContext {...methods}>
      <FormContext.Provider value={{ disabled, id }}>
        <form
          id={id}
          onSubmit={
            onSubmit &&
            methods.handleSubmit(async (data, event) => {
              if (disabled) {
                event?.preventDefault()
                return
              }

              return await onSubmit({
                data,
                event,
                clearError: methods.clearError,
                setError: (name: string, type: string, message?: string) =>
                  methods.setError(name, type, message),
              })
            })
          }
        >
          {children}
        </form>
      </FormContext.Provider>
    </HookFormContext>
  )
}

export default Form
