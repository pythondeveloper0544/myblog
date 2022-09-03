const list = document.querySelectorAll(".nav li");

function activeLink() {
    list.forEach((item) =>
        item.classList.remove('hovered'));
        this.classList.add('hovered');
}

list.forEach((item) =>
    item.addEventListener('mouseover', activeLink)
)

const toggle = document.querySelector('.toggle');
const nav = document.querySelector('.nav');
const main = document.querySelector('.main')

toggle.onclick = function() {
    nav.classList.toggle('active')
    main.classList.toggle('active')
}

const createBtn = document.querySelector('.createBtn');
const topic = document.querySelector('.topic');

createBtn.onclick = function () {
    topic.classList.toggle('active')
}

