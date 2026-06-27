document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('nav');
  const content = document.getElementById('content');
  const searchBox = document.querySelector('.search-box');
  let currentSection = 'riassunto';

  function linkify(text) {
    const linkable = {};
    ['npc', 'luoghi', 'fazioni', 'pg'].forEach(section => {
      DATA[section].forEach(item => {
        linkable[item.title] = section;
      });
    });
    // Sort by length descending to match longer names first
    const names = Object.keys(linkable).sort((a, b) => b.length - a.length);
    names.forEach(name => {
      const escaped = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const re = new RegExp(`(?<!<[^>]*)\\b(${escaped})\\b(?![^<]*>)`, 'g');
      text = text.replace(re, `<a href="#" class="card-link" data-section="${linkable[name]}" data-name="${name}">$1</a>`);
    });
    return text;
  }

  function renderCards(items, filter = '') {
    const f = filter.toLowerCase();
    return items
      .filter(item => !f || item.title.toLowerCase().includes(f) ||
        item.text.toLowerCase().includes(f) ||
        (item.tags || []).some(t => t.toLowerCase().includes(f)))
      .map(item => `
        <div class="card" id="card-${item.title.replace(/[^a-zA-Z0-9]/g, '_')}">
          <h3>${item.title}</h3>
          ${item.meta ? `<div class="meta">${item.meta}</div>` : ''}
          <p>${linkify(item.text)}</p>
          ${item.tags ? `<div style="margin-top:0.5rem">${item.tags.map(t => `<span class="tag">${t}</span>`).join('')}</div>` : ''}
        </div>
      `).join('') || '<p style="color:#888">Nessun risultato.</p>';
  }

  function render(filter = '') {
    content.innerHTML = renderCards(DATA[currentSection], filter);
  }

  nav.addEventListener('click', e => {
    if (e.target.tagName !== 'BUTTON') return;
    nav.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    currentSection = e.target.dataset.section;
    searchBox.value = '';
    render();
  });

  searchBox.addEventListener('input', e => render(e.target.value));

  // Card links navigation
  document.addEventListener('click', e => {
    if (e.target.classList.contains('card-link')) {
      e.preventDefault();
      const section = e.target.dataset.section;
      const name = e.target.dataset.name;
      nav.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      nav.querySelector(`[data-section="${section}"]`).classList.add('active');
      currentSection = section;
      searchBox.value = name;
      render(name);
    }
  });

  // Spoiler toggle
  document.addEventListener('click', e => {
    if (e.target.classList.contains('spoiler')) e.target.classList.toggle('revealed');
  });

  render();
});
