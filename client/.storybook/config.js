import { configure } from '@storybook/react';

import '../src/styles/index.scss';

// automatically import all files ending in *.stories.js
configure(require.context('../src/stories', true, /\.stories\.tsx$/), module);
