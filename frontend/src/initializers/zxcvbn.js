import misago from "misago/index"
import include from "misago/services/include"
import zxcvbn from "misago/services/zxcvbn"

export default function initializer() {
  zxcvbn.init(include)
}

misago.addInitializer({
  name: "zxcvbn",
  initializer: initializer,
})
