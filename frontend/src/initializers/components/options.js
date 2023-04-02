import misago from "misago/index"
import Options, { paths } from "../../components/options/root"
import mount from "../../utils/routed-component"

export default function initializer(context) {
  if (context.has("USER_OPTIONS")) {
    mount({
      basepath: misago.get("USERCP_URL"),
      component: Options,
      paths: paths(),
    })
  }
}

misago.addInitializer({
  name: "component:options",
  initializer: initializer,
  after: "store",
})
