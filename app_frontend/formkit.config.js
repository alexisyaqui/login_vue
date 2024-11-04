import {generateClasses} from '@formkit/themes'


const config = {
  config: {
    classes: generateClasses({
        global: {
            wrapper: 'space-0-1 mb-0',
            message: 'text-red-500 text-center text-sm font-bold uppercase',
            label: 'block text-sm from-neutral-900 text-black-950 uppercase',
            input: 'block w-full py-3 px-0 mt-2 mb-4 text-gray-800 appearance-none border-b-2 border-gray-100 focus:text-gray-500 focus:outline-none focus:border-gray-200'
        },
        submit: {
            input: '$reset w-full py-3 mt-10 bg-indigo-700 rounded-xl font-extrabold text-white uppercase focus:outline-none hover:bg-indigo-950 hover:shadow-none'

        }
    })

  },
};

export default config;

