import { i18n } from "@lingui/core"
import { I18nProvider } from "@lingui/react"
import { en } from 'make-plural/plurals'
import { MemoryRouter } from "react-router-dom"
import messages from "../src/locale/en/messages"
import "../src/styles/index.scss"

i18n.loadLocaleData(en, { plurals: en })
i18n.load("end", messages)
i18n.activate("en")

export const decorators = [
  (Story) => <MemoryRouter><Story /></MemoryRouter>,
  (Story) => (
    <I18nProvider i18n={i18n}>
      <Story />
    </I18nProvider>
  ),
]