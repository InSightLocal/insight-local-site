document.documentElement.classList.add('js');

const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const closeMenu = () => {
  navigation?.classList.remove('open');
  toggle?.setAttribute('aria-expanded', 'false');
};
toggle?.addEventListener('click', () => {
  const open = toggle.getAttribute('aria-expanded') !== 'true';
  toggle.setAttribute('aria-expanded', String(open));
  navigation?.classList.toggle('open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    toggle.focus();
  }
});
navigation?.addEventListener('click', event => {
  if (event.target.closest('a')) closeMenu();
});
const desktopMenu = window.matchMedia('(min-width: 901px)');
if (desktopMenu.addEventListener) {
  desktopMenu.addEventListener('change', event => { if (event.matches) closeMenu(); });
} else if (desktopMenu.addListener) {
  desktopMenu.addListener(event => { if (event.matches) closeMenu(); });
}

// Formulaire sans base de données : préparation du mail ou copie locale.
const form = document.getElementById('mission-form');
const status = document.getElementById('mission-status');
const preview = document.getElementById('mail-preview');
const previewText = document.getElementById('mail-preview-text');

function makeMessage() {
  const data = new FormData(form);
  const value = key => String(data.get(key) || '').trim();
  const rows = [
    ['Nom', value('nom')],
    ['Adresse e-mail', value('email')],
    ['Entreprise', value('entreprise')],
    ['Téléphone', value('tel')],
    ['Type de mission', value('type')],
    ['Zone d’intervention', value('zone')],
    ['Échéance', value('echeance')],
    ['Description de la demande', value('message')]
  ];
  const subject = 'Demande de mission InSight Local — ' + value('type');
  const body = 'Bonjour,\n\nJe vous contacte pour une mission terrain.\n\n'
    + rows.map(([label, text]) => label + ' : ' + (text || 'Non précisé')).join('\n')
    + '\n\nCordialement,\n' + value('nom');
  return { subject, body };
}

form?.addEventListener('submit', event => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const { subject, body } = makeMessage();
  if (status) status.textContent = 'Votre messagerie va s’ouvrir : le message ne partira que lorsque vous validerez son envoi.';
  window.location.href = 'mailto:insight.local@icloud.com?subject='
    + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
});

document.getElementById('copy-mission')?.addEventListener('click', async () => {
  if (!form?.reportValidity()) return;
  const { subject, body } = makeMessage();
  const fullMessage = 'Destinataire : insight.local@icloud.com\nObjet : ' + subject + '\n\n' + body;
  if (preview && previewText) {
    preview.hidden = false;
    previewText.value = fullMessage;
  }
  try {
    if (!navigator.clipboard?.writeText) throw new Error('Presse-papiers indisponible');
    await navigator.clipboard.writeText(fullMessage);
    if (status) status.textContent = 'Demande copiée. Collez-la dans votre messagerie, puis envoyez-la.';
  } catch {
    previewText?.focus();
    previewText?.select();
    if (status) status.textContent = 'Le texte est affiché ci-dessous : copiez-le et envoyez-le depuis votre messagerie.';
  }
});
