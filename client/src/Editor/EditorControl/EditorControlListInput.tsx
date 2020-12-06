import { Trans } from "@lingui/macro"
import React from "react"
import { useFormContext } from "react-hook-form"
import { ButtonPrimary, ButtonSecondary } from "../../UI/Button"
import { useFieldContext } from "../../UI/Form"

const EditorControlListInput: React.FC = () => {
  const context = useFieldContext()
  const { getValues, register, setValue, watch } = useFormContext()
  const name = context && context.name
  const defaultValue: Array<string> = name ? getValues(name) : [""]
  const value: Array<string> = name ? watch(name, defaultValue) : defaultValue

  React.useEffect(() => {
    if (name) register(name)
  }, [name, register])

  if (!name || !setValue) return null

  return (
    <div>
      {value.map((item, index) => (
        <div className="form-group" key={index}>
          <div className="form-row">
            <div className="col">
              <input
                className="form-control"
                type="text"
                value={item}
                onChange={(event) => {
                  const newValue = [...value]
                  newValue[index] = event.target.value
                  setValue(name, newValue)
                }}
              />
            </div>
            <div className="col-auto">
              <ButtonSecondary
                icon="fas fa-times"
                onClick={() => {
                  if (value.length > 1) {
                    const newValue = value.filter((_, i) => i !== index)
                    setValue(name, newValue)
                  }
                }}
              />
            </div>
          </div>
        </div>
      ))}
      <ButtonPrimary
        icon="fas fa-plus"
        text={<Trans id="editor.list_modal.list">Add item</Trans>}
        small
        onClick={() => {
          const newValue = [...value]
          newValue.push("")
          setValue(name, newValue)
        }}
      />
    </div>
  )
}

export default EditorControlListInput
