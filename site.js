const b=document.querySelector('.mobile'),m=document.querySelector('.menu');
if(b&&m){b.addEventListener('click',()=>{const open=m.classList.toggle('open');b.setAttribute('aria-expanded',open?'true':'false');b.textContent=open?'×':'☰';});}
