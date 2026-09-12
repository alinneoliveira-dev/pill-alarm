console.log("Pill Alarm frontend carregado.");


let medicationToDelete = null;


/* =========================================================
   CARREGAR MEDICAÇÕES
========================================================= */

async function loadMedications() {

    const medicationsList =
        document.getElementById("medications-list");

    const medicationCount =
        document.getElementById("medication-count");

    const nextTime =
        document.getElementById("next-time");

    if (!medicationsList) {
        return;
    }

    try {

        const response =
            await fetch("/medications");

        if (!response.ok) {
            throw new Error(
                "Erro ao buscar medicações."
            );
        }

        const data =
            await response.json();

        const medications =
            data.medications;

        medicationCount.textContent =
            medications.length;

        medicationsList.innerHTML = "";

        if (medications.length === 0) {

            medicationsList.innerHTML = `
                <div class="empty-state">

                    <h3>
                        Nenhuma medicação cadastrada
                    </h3>

                    <p>
                        Adicione uma medicação para começar sua rotina.
                    </p>

                </div>
            `;

            nextTime.textContent =
                "--:--";

            return;
        }


        let allTimes = [];


        medications.forEach(
            medication => {

                const schedules =
                    medication.schedules || [];


                schedules.forEach(
                    time => {

                        allTimes.push(time);

                    }
                );


                const schedulesHTML =
                    schedules.length > 0

                        ? schedules
                            .map(
                                time =>
                                    `<strong>${time}</strong>`
                            )
                            .join(" · ")

                        : "<strong>Sem horário cadastrado</strong>";


                const instructionsHTML =
                    medication.instructions

                        ? `<strong>${medication.instructions}</strong>`

                        : "<strong>Sem instruções</strong>";


                const card =
                    document.createElement("article");

                card.className =
                    "medication-card";


                card.innerHTML = `

                    <div class="medication-header">

                        <div class="medication-icon">

                            <img
                                src="/static/assets/icons8-pilula-40.png"
                                alt="Ícone de medicação"
                            >

                        </div>


                        <div class="medication-info">

                            <h3>
                                ${medication.name}
                            </h3>

                            <p>
                                ${
                                    medication.dosage ||
                                    "Dosagem não informada"
                                }
                            </p>

                        </div>

                    </div>


                    <div class="medication-details">

                        <div class="detail">

                            <div>

                                <small>
                                    Horários
                                </small>

                                <div>
                                    ${schedulesHTML}
                                </div>

                            </div>

                        </div>


                        <div class="detail">

                            <span></span>

                            <div>

                                <small>
                                    Instruções
                                </small>

                                ${instructionsHTML}

                            </div>

                        </div>

                    </div>


                    <div class="card-actions">

                        <button
                            type="button"
                            class="secondary-button edit-button"
                            data-id="${medication.id}">

                            Editar

                        </button>


                        <button
                            type="button"
                            class="delete-button"
                            data-id="${medication.id}"
                            data-name="${medication.name}">

                            Excluir

                        </button>

                    </div>
                `;


                medicationsList.appendChild(card);

            }
        );


        if (allTimes.length > 0) {

            allTimes.sort();

            nextTime.textContent =
                allTimes[0];

        } else {

            nextTime.textContent =
                "--:--";

        }

    } catch (error) {

        console.error(error);

        medicationsList.innerHTML = `

            <div class="empty-state">

                <h3>
                    Não foi possível carregar as medicações
                </h3>

                <p>
                    Verifique se o servidor Flask está funcionando.
                </p>

            </div>

        `;
    }
}


/* =========================================================
   DATA ATUAL
========================================================= */

function updateCurrentDate() {

    const currentDate =
        document.getElementById(
            "current-date"
        );

    if (!currentDate) {
        return;
    }

    const today =
        new Date();

    const options = {
        day: "2-digit",
        month: "short"
    };

    currentDate.textContent =
        today.toLocaleDateString(
            "pt-BR",
            options
        );
}


/* =========================================================
   BOTÃO ADICIONAR
========================================================= */

function setupAddButton() {

    const addButton =
        document.querySelector(
            ".add-button"
        );

    if (!addButton) {
        return;
    }

    addButton.addEventListener(
        "click",
        () => {

            window.location.href =
                "/medications/new";

        }
    );
}


/* =========================================================
   BOTÃO EDITAR
========================================================= */

function setupEditButtons() {

    const medicationsList =
        document.getElementById(
            "medications-list"
        );

    if (!medicationsList) {
        return;
    }

    medicationsList.addEventListener(
        "click",
        (event) => {

            const editButton =
                event.target.closest(
                    ".edit-button"
                );

            if (!editButton) {
                return;
            }

            const medicationId =
                editButton.dataset.id;

            window.location.href =
                `/medications/${medicationId}/edit`;

        }
    );
}


/* =========================================================
   CARREGAR DADOS DA MEDICAÇÃO PARA EDIÇÃO
========================================================= */

async function loadMedicationForEdit(
    medicationId
) {

    try {

        const response =
            await fetch(
                `/medications/${medicationId}`
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.message ||
                "Não foi possível carregar a medicação."
            );

        }


        document.getElementById(
            "name"
        ).value =
            data.name || "";


        document.getElementById(
            "dosage"
        ).value =
            data.dosage || "";


        document.getElementById(
            "instructions"
        ).value =
            data.instructions || "";


        /*
         * O backend retorna os horários
         * como objetos:
         *
         * [
         *   {
         *      id: 1,
         *      time: "17:40"
         *   }
         * ]
         *
         * Pegamos o primeiro horário.
         */

        if (
            data.schedules &&
            data.schedules.length > 0
        ) {

            document.getElementById(
                "time"
            ).value =
                data.schedules[0].time;

        }

    } catch (error) {

        console.error(error);

        const message =
            document.getElementById(
                "form-message"
            );

        message.textContent =
            error.message;

        message.style.display =
            "block";

        message.style.background =
            "#fef2f2";

        message.style.color =
            "#991b1b";

    }
}


/* =========================================================
   FORMULÁRIO DE MEDICAÇÃO
========================================================= */

function setupMedicationForm() {

    const form =
        document.getElementById(
            "medication-form"
        );

    if (!form) {
        return;
    }


    const editMode =
        form.dataset.editMode === "true";


    const medicationId =
        form.dataset.medicationId;


    /*
     * Se estiver editando,
     * busca os dados atuais no backend.
     */

    if (
        editMode &&
        medicationId
    ) {

        loadMedicationForEdit(
            medicationId
        );

    }


    form.addEventListener(
        "submit",
        async (event) => {

            event.preventDefault();


            const name =
                document
                    .getElementById("name")
                    .value
                    .trim();


            const dosage =
                document
                    .getElementById("dosage")
                    .value
                    .trim();


            const instructions =
                document
                    .getElementById("instructions")
                    .value
                    .trim();


            const time =
                document
                    .getElementById("time")
                    .value;


            const message =
                document.getElementById(
                    "form-message"
                );


            const saveButton =
                document.getElementById(
                    "save-button"
                );


            if (!name) {

                message.textContent =
                    "Informe o nome da medicação.";

                message.style.display =
                    "block";

                message.style.background =
                    "#fef2f2";

                message.style.color =
                    "#991b1b";

                return;
            }


            if (!time) {

                message.textContent =
                    "Informe o horário da medicação.";

                message.style.display =
                    "block";

                message.style.background =
                    "#fef2f2";

                message.style.color =
                    "#991b1b";

                return;
            }


            saveButton.disabled =
                true;


            saveButton.textContent =
                editMode
                    ? "Salvando..."
                    : "Cadastrando...";


            try {

                /*
                 * ==========================================
                 * MODO EDIÇÃO
                 * ==========================================
                 */

                if (editMode) {

                    const medicationResponse =
                        await fetch(
                            `/medications/${medicationId}`,
                            {
                                method: "PUT",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({

                                    name: name,

                                    dosage:
                                        dosage || null,

                                    instructions:
                                        instructions || null

                                })
                            }
                        );


                    const medicationData =
                        await medicationResponse.json();


                    if (!medicationResponse.ok) {

                        throw new Error(
                            medicationData.message ||
                            "Não foi possível atualizar a medicação."
                        );

                    }


                    /*
                     * Busca a medicação novamente
                     * para descobrir o ID do horário.
                     */

                    const currentMedicationResponse =
                        await fetch(
                            `/medications/${medicationId}`
                        );


                    const currentMedication =
                        await currentMedicationResponse.json();


                    if (
                        !currentMedicationResponse.ok
                    ) {

                        throw new Error(
                            "Medicação atualizada, mas não foi possível carregar o horário."
                        );

                    }


                    if (
                        !currentMedication.schedules ||
                        currentMedication.schedules.length === 0
                    ) {

                        /*
                         * Caso não exista horário,
                         * cria um novo.
                         */

                        const scheduleResponse =
                            await fetch(
                                "/schedules",
                                {
                                    method: "POST",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({

                                        medication_id:
                                            Number(medicationId),

                                        time:
                                            `${time}:00`

                                    })
                                }
                            );


                        const scheduleData =
                            await scheduleResponse.json();


                        if (!scheduleResponse.ok) {

                            throw new Error(
                                scheduleData.message ||
                                "Medicação atualizada, mas o horário não pôde ser salvo."
                            );

                        }

                    } else {

                        /*
                         * Atualiza o primeiro horário existente.
                         */

                        const scheduleId =
                            currentMedication
                                .schedules[0]
                                .id;


                        const scheduleResponse =
                            await fetch(
                                `/schedules/${scheduleId}`,
                                {
                                    method: "PUT",

                                    headers: {
                                        "Content-Type":
                                            "application/json"
                                    },

                                    body: JSON.stringify({

                                        time:
                                            `${time}:00`

                                    })
                                }
                            );


                        const scheduleData =
                            await scheduleResponse.json();


                        if (!scheduleResponse.ok) {

                            throw new Error(
                                scheduleData.message ||
                                "Medicação atualizada, mas o horário não pôde ser atualizado."
                            );

                            }

                    }


                    message.textContent =
                        "Medicação atualizada com sucesso!";

                    message.style.display =
                        "block";

                    message.style.background =
                        "#ecfdf3";

                    message.style.color =
                        "#166534";


                    setTimeout(
                        () => {

                            window.location.href =
                                "/dashboard";

                        },
                        800
                    );


                    return;
                }


                /*
                 * ==========================================
                 * MODO CADASTRO
                 * ==========================================
                 */

                const medicationResponse =
                    await fetch(
                        "/medications",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                user_id: 1,

                                name: name,

                                dosage:
                                    dosage || null,

                                instructions:
                                    instructions || null

                            })
                        }
                    );


                const medicationData =
                    await medicationResponse.json();


                if (!medicationResponse.ok) {

                    throw new Error(
                        medicationData.message ||
                        "Não foi possível cadastrar a medicação."
                    );

                }


                const newMedicationId =
                    medicationData.medication.id;


                const scheduleResponse =
                    await fetch(
                        "/schedules",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                medication_id:
                                    newMedicationId,

                                time:
                                    `${time}:00`

                            })
                        }
                    );


                const scheduleData =
                    await scheduleResponse.json();


                if (!scheduleResponse.ok) {

                    throw new Error(
                        scheduleData.message ||
                        "A medicação foi criada, mas o horário não pôde ser salvo."
                    );

                }


                message.textContent =
                    "Medicação cadastrada com sucesso!";

                message.style.display =
                    "block";

                message.style.background =
                    "#ecfdf3";

                message.style.color =
                    "#166534";


                setTimeout(
                    () => {

                        window.location.href =
                            "/dashboard";

                    },
                    800
                );

            } catch (error) {

                console.error(error);

                message.textContent =
                    error.message;

                message.style.display =
                    "block";

                message.style.background =
                    "#fef2f2";

                message.style.color =
                    "#991b1b";

            } finally {

                saveButton.disabled =
                    false;

                saveButton.textContent =
                    editMode
                        ? "Salvar alterações"
                        : "Salvar medicação";

            }

        }
    );
}


/* =========================================================
   MODAL DE EXCLUSÃO
========================================================= */

function openDeleteModal(
    medicationId,
    medicationName
) {

    const modal =
        document.getElementById(
            "delete-modal"
        );

    const medicationNameElement =
        document.getElementById(
            "delete-medication-name"
        );


    medicationToDelete =
        medicationId;


    medicationNameElement.textContent =
        medicationName;


    modal.classList.add(
        "active"
    );


    modal.setAttribute(
        "aria-hidden",
        "false"
    );
}


function closeDeleteModal() {

    const modal =
        document.getElementById(
            "delete-modal"
        );


    medicationToDelete =
        null;


    modal.classList.remove(
        "active"
    );


    modal.setAttribute(
        "aria-hidden",
        "true"
    );
}


/* =========================================================
   EXCLUIR MEDICAÇÃO
========================================================= */

async function deleteMedication() {

    if (!medicationToDelete) {
        return;
    }


    const medicationId =
        medicationToDelete;


    const confirmButton =
        document.getElementById(
            "confirm-delete"
        );


    confirmButton.disabled =
        true;


    confirmButton.textContent =
        "Excluindo...";


    try {

        const response =
            await fetch(
                `/medications/${medicationId}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "Não foi possível excluir a medicação."
            );

        }


        closeDeleteModal();


        await loadMedications();


    } catch (error) {

        console.error(error);

        closeDeleteModal();

        showErrorMessage(
            error.message
        );

    } finally {

        confirmButton.disabled =
            false;

        confirmButton.textContent =
            "Excluir medicação";

    }
}


/* =========================================================
   CONFIGURAR MODAL
========================================================= */

function setupDeleteModal() {

    const medicationsList =
        document.getElementById(
            "medications-list"
        );


    const cancelButton =
        document.getElementById(
            "cancel-delete"
        );


    const confirmButton =
        document.getElementById(
            "confirm-delete"
        );


    const modal =
        document.getElementById(
            "delete-modal"
        );


    if (
        !medicationsList ||
        !cancelButton ||
        !confirmButton ||
        !modal
    ) {
        return;
    }


    medicationsList.addEventListener(
        "click",
        (event) => {

            const deleteButton =
                event.target.closest(
                    ".delete-button"
                );


            if (!deleteButton) {
                return;
            }


            const medicationId =
                deleteButton.dataset.id;


            const medicationName =
                deleteButton.dataset.name;


            openDeleteModal(
                medicationId,
                medicationName
            );

        }
    );


    cancelButton.addEventListener(
        "click",
        () => {

            closeDeleteModal();

        }
    );


    confirmButton.addEventListener(
        "click",
        () => {

            deleteMedication();

        }
    );


    modal.addEventListener(
        "click",
        (event) => {

            if (
                event.target === modal
            ) {

                closeDeleteModal();

            }

        }
    );


    document.addEventListener(
        "keydown",
        (event) => {

            if (
                event.key === "Escape" &&
                modal.classList.contains("active")
            ) {

                closeDeleteModal();

            }

        }
    );
}


/* =========================================================
   MENSAGEM DE ERRO TEMPORÁRIA
========================================================= */

function showErrorMessage(
    message
) {

    const errorMessage =
        document.createElement(
            "div"
        );


    errorMessage.className =
        "temporary-error-message";


    errorMessage.textContent =
        message;


    document.body.appendChild(
        errorMessage
    );


    setTimeout(
        () => {

            errorMessage.remove();

        },
        4000
    );
}


/* =========================================================
   INICIALIZAÇÃO
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        updateCurrentDate();

        loadMedications();

        setupAddButton();

        setupEditButtons();

        setupMedicationForm();

        setupDeleteModal();

    }
);