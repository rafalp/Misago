import misago from 'misago/index';
import include from 'misago/services/include';
import dropzone from 'misago/services/dropzone';

export default function initializer() {
  dropzone.init(include);
}

misago.addInitializer({
  name: 'dropzone',
  initializer: initializer
});
