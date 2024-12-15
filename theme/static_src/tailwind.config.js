/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
      spacing: {
        0.5: '0.12rem',
        layout: '1.4rem',
        'big-layout': '2.3rem'
      },
      fontSize: {
        xs: '0.9rem',
        sm: '1.07rem',
        base: '1.18rem',
        lg: '1.24rem',
        xl: '1.38rem',
        '1.5xl': '1.5rem',
        '2xl': '1.82rem',
        '3xl': '2.22rem',
        '4xl': '2.66rem',
        '5xl': '3.56rem',
        '6xl': '4.44rem',
        '7xl': '5.33rem',
        '8xl': '7.1rem',
        '9xl': '9.5rem'
      },
      transitionDuration: {
        DEFAULT: '266ms'
      },
      width: {
        '1p': '1%',
        '2p': '2%',
        '3p': '3%',
        '4p': '4%',
        '5p': '5%',
        '6p': '6%',
        '7p': '7%',
        '8p': '8%',
        '9p': '9%',
        '10p': '10%',
        '11p': '11%',
        '12p': '12%',
        '13p': '13%',
        '14p': '14%',
        '15p': '15%',
        '16p': '16%',
        '17p': '17%',
        '18p': '18%',
        '19p': '19%',
        '20p': '20%',
        '21p': '21%',
        '22p': '22%',
        '23p': '23%',
        '24p': '24%',
        '25p': '25%',
        '26p': '26%',
        '27p': '27%',
        '28p': '28%',
        '29p': '29%',
        '30p': '30%',
        '31p': '31%',
        '32p': '32%',
        '33p': '33%',
        '34p': '34%',
        '35p': '35%',
        '36p': '36%',
        '37p': '37%',
        '38p': '38%',
        '39p': '39%',
        '40p': '40%',
        '41p': '41%',
        '42p': '42%',
        '43p': '43%',
        '44p': '44%',
        '45p': '45%',
        '46p': '46%',
        '47p': '47%',
        '48p': '48%',
        '49p': '49%',
        '50p': '50%',
        '51p': '51%',
        '52p': '52%',
        '53p': '53%',
        '54p': '54%',
        '55p': '55%',
        '56p': '56%',
        '57p': '57%',
        '58p': '58%',
        '59p': '59%',
        '60p': '60%',
        '61p': '61%',
        '62p': '62%',
        '63p': '63%',
        '64p': '64%',
        '65p': '65%',
        '66p': '66%',
        '67p': '67%',
        '68p': '68%',
        '69p': '69%',
        '70p': '70%',
        '71p': '71%',
        '72p': '72%',
        '73p': '73%',
        '74p': '74%',
        '75p': '75%',
        '76p': '76%',
        '77p': '77%',
        '78p': '78%',
        '79p': '79%',
        '80p': '80%',
        '81p': '81%',
        '82p': '82%',
        '83p': '83%',
        '84p': '84%',
        '85p': '85%',
        '86p': '86%',
        '87p': '87%',
        '88p': '88%',
        '89p': '89%',
        '90p': '90%',
        '91p': '91%',
        '92p': '92%',
        '93p': '93%',
        '94p': '94%',
        '95p': '95%',
        '96p': '96%',
        '97p': '97%',
        '98p': '98%',
        '99p': '99%'
      },
            fontFamily: {
                minecraft: ["MinecraftFont"],
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
