// main.html

 function loadContent(pagina) {
        fetch(`/content/${pagina}`)
            .then(res => res.text())
            .then(html => {
                document.getElementById('main-section').innerHTML = html;
            })
            .catch(() => {
                document.getElementById('main-section').innerHTML = "<p>Erro ao carregar conteúdo</p>";
            });
    }

document.addEventListener("DOMContentLoaded", function () {

        const profileMenu = document.getElementById('profileMenu')
        const profilePic = document.getElementById('profilepic')

        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener("click", function () {
                document.querySelectorAll('.menu-item').forEach(i => {
                    if (i !== item) i.classList.remove('active')
                })
                item.classList.toggle('active')
            })
        })

        profilePic.addEventListener("click", function () {
            if (profileMenu.style.display !== 'none' && profileMenu.style.display !== '') {
                profileMenu.style.display = 'none'
            } else {
                profileMenu.style.display = 'flex'
            }
        })
        
        
//menu-lateral.html
    const registro = document.getElementById('regFunc')
    const main = document.getElementById('main-section')

        registro.addEventListener('click', () => {
            fetch('/content/addUser')
                .then(r => r.text())
                .then(html => {
                    main.innerHTML = html
                })
        })
        
        const funcs = document.getElementById('funcList')
        funcs.addEventListener('click', () => {
            fetch('/funcList')
            .then(r => r.text())
            .then(html => {
                main.innerHTML = html
            })
            .catch(error => {
                console.error('Erro ao carregar lista de funcionários:', error)
            })
        })
    })