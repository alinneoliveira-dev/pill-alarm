console.log("Pill Alarm frontend carregado.");

const addButton = document.querySelector(".add-button");

if (addButton) {
    addButton.addEventListener("click", () => {
        console.log("Botão de adicionar clicado.");
    });
}