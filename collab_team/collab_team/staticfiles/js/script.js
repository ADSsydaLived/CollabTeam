function changeLanguage(lang) {
        document.getElementById('languageInput').value = lang;
        document.getElementById('languageForm').submit();
    }

const passwordInput = document.querySelector('#id_password1');
const passwordHints = document.getElementById('password-hints');

passwordInput.addEventListener('focus', function() {
  passwordHints.style.display = 'block';
});

passwordInput.addEventListener('blur', function() {
  passwordHints.style.display = 'none';
});

const close_project = document.getElementById("closeProjectButton");

close_project.addEventListener("click", function() {
    fetch("{% url 'close_project' project.id %}", {
        method: "POST",
        headers: {
            "X-CSRFToken": "{{ csrf_token }}",
        }
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            alert("Ошибка при закрытии проекта.");
        }
    });
});

const button = document.getElementById('myButton');
button.addEventListener('click', function() {
    console.log('Button clicked!');
});

function addClassToEverySecondItem(){
    const comm_dec = document.getElementByClassName('comments-section');
    const items = Array.from(container.getElementsByName('div'));

    items.forEach((item, index) => {
        if (index % 2 === 1) {
            item.style.text-align = 'end';
            item.style.transform = 'translate(21%, 0px)';
        }
        else {
            item.style.text-align = 'start';
            item.style.transform = 'translate(21%, 0px)';
        }
    });
}
window.onload = addClassToEverySecondItem;