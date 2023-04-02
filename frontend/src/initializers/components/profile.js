import { connect } from "react-redux"
import misago from "misago/index"
import Profile, { paths, select } from "../../components/profile/root"
import mount from "../../utils/routed-component"

export default function initializer(context) {
  if (context.has("PROFILE") && context.has("PROFILE_PAGES")) {
    mount({
      basepath: misago.get("PROFILE").url,
      component: connect(select)(Profile),
      paths: paths(),
    })
  }
}

misago.addInitializer({
  name: "component:profile",
  initializer: initializer,
  after: "reducer:profile-hydrate",
})
