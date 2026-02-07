/**
 * Sidebar configuration for Physical AI & Humanoid Robotics Textbook
 * Auto-generated navigation based on frontmatter sidebar_position
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Chapters',
      collapsible: true,
      collapsed: false,
      items: [
        'chapter-01/chapter-01',
        'chapter-02/chapter-02',
        'chapter-03/chapter-03',
        'chapter-04/chapter-04',
        'chapter-05/chapter-05',
        'chapter-06/chapter-06',
      ],
    },
  ],
};

module.exports = sidebars;
