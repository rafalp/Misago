import React from "react"
import {
  FieldValues,
  FormContext as HookFormContext,
  IsFlatObject,
  ManualFieldError,
  Message,
  MultipleFieldErrors,
  useForm,
} from "react-hook-form"
import { FormContext } from "./FormContext"

interface IOnSubmit<FormValues extends FieldValues = FieldValues> {
  data: FormValues
  event?: React.BaseSyntheticEvent<object, any, any>
  clearError: (
    name?:
      | (IsFlatObject<FormValues> extends true
          ? Extract<keyof FormValues, string>
          : string)
      | (IsFlatObject<FormValues> extends true
          ? Extract<keyof FormValues, string>
          : string)[]
  ) => void
  setError(
    name: IsFlatObject<FormValues> extends true
      ? Extract<keyof FormValues, string>
      : string,
    type: MultipleFieldErrors
  ): void
  setError(
    name: IsFlatObject<FormValues> extends true
      ? Extract<keyof FormValues, string>
      : string,
    type: string,
    message?: Message
  ): void
  setError(name: ManualFieldError<FormValues>[]): void
}

interface IFormProps<FormValues> {
  children?: React.ReactNode
  className?: string
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
    className,
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
          className={className}
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
                setError: methods.setError,
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
