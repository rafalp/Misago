import { paths } from "misago/components/thread/root"
import misago from "misago/index"
import mount from "misago/utils/routed-component"

export default function initializer(context) {
  if (context.has("THREAD") && context.has("POSTS")) {
    mount({
      paths: paths(),
    })
  }
}

misago.addInitializer({
  name: "component:thread",
  initializer: initializer,
  after: "store",
})
