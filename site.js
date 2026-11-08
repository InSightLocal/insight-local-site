const toggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() { navigation?.classList.remove('open'); toggle?.setAttribute('aria-expanded', 'false'); }
toggle?.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') !== 'true'; toggle.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('open', open); });
document.addEventListener('keydown', event => { if(event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') { closeMenu(); toggle.focus(); } });
navigation?.addEventListener('click', event => { if(event.target.closest('a')) closeMenu(); });
window.matchMedia('(min-width: 801px)').addEventListener('change', event => { if(event.matches) closeMenu(); });

// Le formulaire prépare un mail dans l'application locale, sans transfert réseau du site.
const form=document.getElementById('mission-form');
form?.addEventListener('submit',e=>{e.preventDefault();if(!form.reportValidity())return;const data=new FormData(form),v=k=>String(data.get(k)||'').trim();const pairs=[['Nom',v('nom')],['E-mail',v('email')],['Entreprise',v('entreprise')],['Téléphone',v('tel')],['Mission',v('type')],['Zone',v('zone')],['Échéance',v('echeance')],['Message',v('message')]];const subject='Demande InSight Local — '+v('type'),body='Bonjour,\n\nJe vous contacte au sujet d’une mission.\n\n'+pairs.map(([a,b])=>a+' : '+(b||'Non précisé')).join('\n')+'\n\nCordialement,\n'+v('nom');const status=document.getElementById('mission-status');if(status)status.textContent='Votre messagerie va s’ouvrir. Vérifiez puis envoyez le courriel depuis celle-ci.';window.location.href='mailto:insight.local@icloud.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);});
// Bandeau de contact présent sur toutes les pages sans dépendance externe.
const dock=document.createElement('aside');dock.className='contact-dock';dock.setAttribute('aria-label','Contact rapide InSight Local');dock.innerHTML='<div class="wrap dock-inner"><span class="dock-caption">Une mission terrain à confier ?</span><a class="dock-link" href="tel:+33679885501">☎ 06 79 88 55 01</a><a class="dock-link" href="mailto:insight.local@icloud.com">✉ insight.local@icloud.com</a><a class="dock-button" href="contact.html">Contact →</a></div>';document.body.appendChild(dock);
