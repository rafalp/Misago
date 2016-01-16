import misago from 'misago/index';
import include from 'misago/services/include';
import cropit from 'misago/services/cropit';

export default function initializer() {
  cropit.init(include);
}

misago.addInitializer({
  name: 'cropit',
  initializer: initializer
});
