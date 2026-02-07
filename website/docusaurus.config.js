const {themes: prismThemes} = require('prism-react-renderer');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'An Interactive Textbook',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-domain.vercel.app',
  baseUrl: '/',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Internationalization
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: '/', // Serve docs at the site's root
          sidebarPath: require.resolve('./sidebars.js'),
          showLastUpdateTime: false,
          showLastUpdateAuthor: false,
        },
        blog: false, // Disable blog
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Metadata
      metadata: [
        {name: 'keywords', content: 'physical ai, humanoid robotics, ai education, robotics course, machine learning, robotics tutorial'},
        {name: 'description', content: 'Learn Physical AI and Humanoid Robotics through an interactive, AI-native textbook. Complete course in under 45 minutes.'},
        {name: 'author', content: 'Physical AI Textbook Team'},
        {property: 'og:type', content: 'website'},
        {property: 'og:title', content: 'Physical AI & Humanoid Robotics - Interactive Textbook'},
        {property: 'og:description', content: 'Learn Physical AI and Humanoid Robotics through an interactive, AI-native textbook. Complete course in under 45 minutes.'},
        {property: 'og:image', content: '/img/docusaurus-social-card.jpg'},
        {name: 'twitter:card', content: 'summary_large_image'},
        {name: 'twitter:title', content: 'Physical AI & Humanoid Robotics'},
        {name: 'twitter:description', content: 'Interactive textbook for learning Physical AI and Humanoid Robotics'},
      ],

      // Open Graph image
      image: 'img/docusaurus-social-card.jpg',

      // Color mode
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },

      // Navbar
      navbar: {
        title: 'Physical AI Textbook',
        hideOnScroll: false,
        items: [],
      },

      // Footer
      footer: {
        style: 'dark',
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
      },

      // Prism syntax highlighting
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'json', 'yaml'],
      },

      // Table of contents
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },
    }),
};

module.exports = config;
